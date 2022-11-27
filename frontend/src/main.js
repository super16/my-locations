import axios from 'axios';
import { createApp } from 'vue'
import './style.css'
import 'leaflet/dist/leaflet.css';
import App from './App.vue'

axios.defaults.baseURL = 'http://api.mylocations.local/v1/';

createApp(App).mount('#app')
