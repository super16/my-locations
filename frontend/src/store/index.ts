import axios from 'axios';
import {
  icon,
  layerGroup,
  map,
  marker,
  Marker,
  tileLayer,
} from 'leaflet';
import markerIcon from 'leaflet/dist/images/marker-icon-2x.png';
import { defineStore } from 'pinia';

import { FieldName, LocationItem, MapStore } from '@/types';

axios.defaults.baseURL = `${import.meta.env.VITE_API_BASE}`;

export const mapStore = defineStore('main', {
  state: (): MapStore => {
    return {
      coordinates: null,
      description: '',
      descriptionInvalid: false,
      errorMessage: '',
      isCreate: false,
      isEdit: false,
      layerGroupId: null,
      locationId: null,
      map: null,
      showDialog: false,
      title: '',
      titleInvalid: false,
      tmpLayerGroupId: null,
    };
  },
  actions: {
    /**
     * POST request to create point.
     */
    async createLocation() {
      this.resetErrors();
      try {
        const { data } = await axios.post('locations', {
          description: this.description,
          latitude: this.coordinates?.lat,
          longitude: this.coordinates?.lng,
          title: this.title,
        });
        this.map.eachLayer((layer: any) => {
          if (layerGroup().getLayerId(layer) === this.layerGroupId) {
            this.createMarker(data).addTo(layer);
          }
        });
      } catch (error: any) {
        const { context, message } = error.response.data;
        context.invalid_fields.forEach((field: FieldName) => {
          this[`${field}Invalid`] = true;
        });
        this.errorMessage = message;
        throw new Error(error);
      }
      this.resetErrors();
      this.resetStore();
    },

    /**
     * Clear temporary markers (used while creating location point).
     */
    removeTemporaryMarkers() {
      this.map.eachLayer((layer: any) => {
        if (layerGroup().getLayerId(layer) === this.tmpLayerGroupId) {
          layer.remove();
        }
      });
    },

    /**
     * Create clickable marker point for adding to map.
     * @param {Object} markerObj - Data object to create marker.
     * @param {number} markerObj.id - Location's id.
     * @param {string} markerObj.title - Location's title.
     * @param {string} markerObj.description - Location's description.
     * @param {number} markerObj.latitude - Location's latitude.
     * @param {number} markerObj.longitude - Location's longitude.
     */
    createMarker(markerObj: LocationItem) {
      const newMarker = marker(
        [markerObj.latitude, markerObj.longitude],
        {
          // @ts-ignore: ToDo: extend Marker type
          description: markerObj.description,
          locationId: markerObj.id,
          title: markerObj.title,
        },
      );
      newMarker.on('click', async (e) => {
        const { locationId } = e.sourceTarget.options;
        this.locationId = locationId;
        this.fetchOneLocation();
        this.showDialog = true;
      });
      return newMarker;
    },

    /**
     * DELETE request to delete point.
     */
    async deleteLocation() {
      this.errorMessage = '';
      try {
        await axios.delete(`/locations/${this.locationId}`);
      } catch (error: any) {
        this.errorMessage = error;
        throw new Error(error);
      }
      this.fetchLocations();
      this.resetErrors();
      this.resetStore();
    },

    /**
     * PATCH request to edit point.
     */
    async editLocation() {
      this.errorMessage = '';
      try {
        await axios.patch(`/locations/${this.locationId}`, {
          description: this.description, title: this.title,
        });
      } catch (error: any) {
        const { context, message } = error.response.data;
        context.invalid_fields.forEach((field: FieldName) => {
          this[`${field}Invalid`] = true;
        });
        this.errorMessage = message;
        throw new Error(error);
      }
      this.fetchLocations();
      this.resetErrors();
      this.resetStore();
    },

    /**
     * Initialize & stylize map to render.
     */
    initMap() {
      // Set defaults for map styling
      Marker.prototype.options.icon = icon({
        className: 'filter',
        iconUrl: markerIcon,
        iconSize: [22, 36],
        iconAnchor: [11, 36],
        popupAnchor: [0, -36],
      });

      this.map = map('map').setView([58, 18], 6);

      tileLayer(
        'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
        { maxZoom: 19 },
      ).addTo(this.map);

      // Move view on map
      this.map.on('moveend', () => this.fetchLocations());

      // Click on map to create new location (add temporary marker)
      this.map.on('click', (e: any) => {
        this.isCreate = true;
        this.removeTemporaryMarkers();
        let tmpLayerGroup = layerGroup().addTo(this.map);
        this.tmpLayerGroupId = layerGroup().getLayerId(tmpLayerGroup);
        const tmpNewMarker = marker([e?.latlng.lat, e?.latlng.lng]);

        tmpNewMarker.setIcon(icon({
          className: 'tmpFilter',
          iconUrl: markerIcon,
          iconSize: [22, 36],
          iconAnchor: [11, 36],
          popupAnchor: [0, -36],
        }));

        tmpNewMarker.addTo(tmpLayerGroup);
        this.coordinates = e?.latlng;
        this.showDialog = true;
      });
    },

    /**
     * GET request for collection of locations.
     */
    async fetchLocations() {
      // eslint-disable-next-line @typescript-eslint/naming-convention
      const { _northEast, _southWest } = this.map.getBounds();
      const params = {
        end_latitude: _northEast.lat,
        end_longitude: _northEast.lng,
        start_latitude: _southWest.lat,
        start_longitude: _southWest.lng,
      };
      try {
        const { data } = await axios.get('locations', { params });

        // Clear all previous markers
        this.map.eachLayer((layer: any) => {
          if (layerGroup().getLayerId(layer) === this.layerGroupId) {
            layer.remove();
          }
        });

        // Put received locations on layer group
        const newLayerGroup = layerGroup().addTo(this.map);
        this.layerGroupId = layerGroup().getLayerId(newLayerGroup);

        data.forEach((location: LocationItem) => {
          const newMarker = this.createMarker(location);
          newMarker.addTo(newLayerGroup);
        });
      } catch (error: any) {
        this.errorMessage = error;
        throw new Error(error);
      }
    },

    /**
     * GET request for location by id.
     */
    async fetchOneLocation() {
      this.errorMessage = '';
      try {
        const { data } = await axios.get(`/locations/${this.locationId}`);
        const { description, title } = data;
        Object.assign(this, { description, title });
      } catch (error: any) {
        this.errorMessage = error;
        throw new Error(error);
      }
    },

    /**
     * Reset Error store values.
     */
    resetErrors() {
      this.descriptionInvalid = false;
      this.titleInvalid = false;
      this.errorMessage = '';
    },

    /**
     * Reset store values after dialog menu close.
     */
    resetStore() {
      this.isCreate = false;
      this.isEdit = false;
      this.coordinates = null;
      this.showDialog = false;
      this.removeTemporaryMarkers();
      this.title = '';
      this.description = '';
    },
  },
});
