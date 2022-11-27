import { createPinia } from 'pinia';
import { createApp } from 'vue';

import 'leaflet/dist/leaflet.css';
import './style.css';

import App from '@/AppComponent.vue';

const pinia = createPinia();

createApp(App).use(pinia).mount('#app');
