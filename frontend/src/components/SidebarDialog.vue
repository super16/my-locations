<script setup lang="ts">
import { storeToRefs } from 'pinia';

import LocationEditor from '@/components/LocationEditor.vue';
import LocationViewer from '@/components/LocationViewer.vue';
import { mapStore } from '@/store';

const store = mapStore();

const { isCreate, isEdit } = storeToRefs(store);
</script>

<template>
  <aside
    id="dialog-menu"
    class="dialog-container flex-column gap-8"
  >
    <header class="flex-center justify-between">
      <h1 class="header-first">
        <template v-if="isCreate">
          New location
        </template>
        <template v-else-if="isEdit">
          Edit location
        </template>
        <template v-else>
          Location
        </template>
      </h1>
      <button
        class="btn-icon flex-center justify-center"
        type="button"
        @click="store.resetStore"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          stroke-width="2"
          class="h-6 stroke-blue-800 w-6"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      </button>
    </header>
    <LocationEditor v-if="isCreate || isEdit" />
    <LocationViewer v-else />
  </aside>
</template>

<style scoped>
#dialog-menu {
  z-index: 1001;
}
</style>
