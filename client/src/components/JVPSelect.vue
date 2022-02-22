<template>
  <div>
    <label :for="id" class="block text-sm font-medium text-gray-700">
      {{ label }}
    </label>
    <select
      :value="item"
      :id="id"
      class="
        mt-1
        block
        w-full
        pl-3
        pr-10
        py-2
        text-base
        border-gray-300
        focus:outline-none focus:ring-indigo-500 focus:border-indigo-500
        sm:text-sm
        rounded-md
      "
      @input="updateItem"
    >
      <option
        v-for="option in options"
        :key="option"
        :name="option"
        :selected="modelValue"
      >
        {{ option }}
      </option>
    </select>
  </div>
</template>

<script>
import { defineComponent, computed } from 'vue';
import inputProps from '../utils/input-props';

export default defineComponent({
  props: {
    options: {
      type: Array,
      required: true,
    },
    ...inputProps,
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const item = computed(() => props.modelValue);
    const updateItem = (e) => emit('update:modelValue', e.target.value);
    return { item, updateItem };
  },
});
</script>
