export interface Coordinates {
  lat: number,
  lng: number,
}

export interface LocationItem {
  id: number,
  latitude: number,
  longitude: number,
  title: string,
  description: string,
}

export interface MapStore {
  coordinates: Coordinates | null,
  description: string,
  descriptionInvalid: boolean,
  errorMessage: string,
  isCreate: boolean,
  isEdit: boolean,
  layerGroupId: number | null,
  locationId: number | null,
  map: any,
  showDialog: boolean,
  title: string,
  titleInvalid: boolean,
  tmpLayerGroupId: number | null,
}

export type FieldName = 'description' | 'title';
