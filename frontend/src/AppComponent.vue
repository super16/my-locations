<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { onMounted } from 'vue';

import { mapStore } from '@/store';
import SidebarDialog from '@/components/SidebarDialog.vue';

const store = mapStore();
const { showDialog } = storeToRefs(store);

onMounted(() => {
  store.initMap();
  store.fetchLocations();
});
</script>

<template>
  <Transition>
    <SidebarDialog v-if="showDialog" />
  </Transition>
  <div
    id="map"
    class="absolute h-screen w-screen"
  />
</template>

<style scoped>
.v-enter-active,
.v-leave-active {
  transition: .5s;
}

.v-enter-from,
.v-leave-to {
  transform: translate(100%, 0);
}
</style>
