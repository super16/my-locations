<script setup lang="ts">
import { storeToRefs  } from 'pinia';

import { mapStore } from '@/store';

const store = mapStore();

const { isEdit, description, title } = storeToRefs(store);
</script>

<template>
  <article class="flex-column gap-6">
    <h2 class="header-second">
      {{ title }}
    </h2>
    <p class="text whitespace-pre-wrap">
      {{ description }}
    </p>
    <button
      class="btn btn-primary"
      type="button"
      @click="isEdit = true"
    >
      <span class="font-semibold text">
        Edit
      </span>
    </button>
    <button
      class="btn btn-danger"
      type="button"
      @click="store.deleteLocation"
    >
      <span class="font-semibold text">
        Delete
      </span>
    </button>
  </article>
</template>
