<script>
import axios from 'axios';
import L from 'leaflet';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

export default {
  name: 'Map',
  data() {
    return {
      latlng: null,
      map: null,
    }
  },
  mounted() {
    let DefaultIcon = L.icon({
      iconUrl: icon,
      shadowUrl: iconShadow
    });
    L.Marker.prototype.options.icon = DefaultIcon;
    this.setupMap();
    this.getLocations();
    this.map.on('click', (e) => {
      this.latlng = e.latlng
      L.Icon.Default.prototype.options.className = 'filter'
      L.marker(
        [e.latlng.lat, e.latlng.lng]
      ).addTo(this.map);
      this.$refs.dialog.show()
      setTimeout(() => this.$refs.dialog.close(), 3500);
    })
    this.map.on('moveend', (e) => {
      this.getLocations();
    })
  },
  methods: {
    setupMap() {
      this.map = L.map('map').setView([58, 18], 6);
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
      }).addTo(this.map);
    },
    getLocations() {
      const { _northEast, _southWest } = this.map.getBounds()
      const params = {
        end_latitude: _northEast.lat,
        end_longitude: _northEast.lng,
        start_latitude: _southWest.lat,
        start_longitude: _southWest.lng,
      };
      axios.get('locations', { params }).then((res) => {
        const { data } = res;
      });
    }
  },
};
</script>

<template>
  <div id="map"></div>
  <dialog
    class="bg-lime-200 border-8 border-black bottom-6 h-20 w-96"
    ref="dialog"
  >
    <span>
      Point has been planted.
    </span>
  </dialog>
</template>

<style scoped>
#map {
  width: 100vw;
  height: 100vh;
}

dialog {
  z-index: 999;
}
</style>
