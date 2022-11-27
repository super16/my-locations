<script setup lang="ts">
import { storeToRefs } from 'pinia';

import { mapStore } from '@/store';

const store = mapStore();

const {
  description,
  descriptionInvalid,
  errorMessage,
  isEdit,
  title,
  titleInvalid,
} = storeToRefs(store);


function submitLocation() {
  if (isEdit.value) {
    store.editLocation();
  } else {
    store.createLocation();
  }
}
</script>

<template>
  <form
    action=""
    method="get"
    class="flex-column gap-6"
  >
    <label
      for="title"
      class="block"
    >
      <span class="font-medium text">
        Title
      </span>
      <input
        v-model="title"
        class="form-input"
        name="title"
        :required="titleInvalid"
        type="text"
      >
    </label>
    <label
      for="description"
      class="block"
    >
      <span class="font-medium text">
        Description
      </span>
      <textarea
        v-model="description"
        class="form-input"
        name="description"
        :required="descriptionInvalid"
        rows="8"
      />
    </label>
    <span
      v-if="errorMessage"
      class="error-message"
    >
      {{ errorMessage }}
    </span>
    <button
      class="btn btn-primary"
      type="button"
      @click="submitLocation"
    >
      <span class="font-semibold text">
        {{ isEdit ? 'Edit' : 'Add' }}
      </span>
    </button>
  </form>
</template>
