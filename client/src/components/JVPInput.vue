<template>
  <div>
    <label :for="id" class="block text-sm font-medium text-gray-700">
      {{ label }}
    </label>
    <div class="mt-1 relative rounded-md shadow-sm">
      <input
        :value="modelValue"
        :type="type"
        :name="id"
        :id="id"
        class="block w-full sm:text-sm rounded-md shadow-sm"
        :class="dynamicClass"
        :aria-invalid="isError"
        :aria-describedby="hintId"
        :autofocus="autofocus"
        @input="updateValue"
        @blur="vuelidate.$touch"
      />
      <div
        v-if="isError"
        class="absolute inset-y-0 right-0 flex items-center pointer-events-none"
        :class="type === 'date' ? 'pr-9' : 'pr-3'"
      >
        <ExclamationCircleIcon
          class="h-5 w-5 text-red-500"
          aria-hidden="true"
        />
      </div>
    </div>
    <p v-if="hasHint" class="mt-0 text-sm" :class="hintClass" :id="hintId">
      {{ hintText }}
    </p>
  </div>
</template>

<script>
import { defineComponent, computed } from 'vue';
import { ExclamationCircleIcon } from '@heroicons/vue/solid';
import inputProps from '../utils/input-props';

export default defineComponent({
  components: { ExclamationCircleIcon },
  props: {
    type: {
      type: String,
      required: false,
      default: 'text',
    },
    placeholder: {
      type: String,
      required: false,
    },
    vuelidate: {
      type: Object,
      required: false,
      default: () => ({}),
    },
    autofocus: {
      type: Boolean,
      required: false,
      default: false,
    },
    ...inputProps,
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    // This is simply cleaner than putting emit code in the HTML
    const updateValue = (e) => emit('update:modelValue', e.target.value);

    // Vuelidate is used as a validation library.
    // We use built-in functionality to determine if any rules are violated
    // as well as display of the associated error text
    const isError = computed(() => props.vuelidate.$error);
    const errorText = computed(() => {
      const messages =
        props.vuelidate.$errors?.map((err) => err.$message) ?? [];
      return messages.join(' ');
    });

    // This is solely to style the input based on whether it is in an error state or not
    const dynamicClass = computed(() => {
      // This is to remove padding on the right for the built-in calendar icon when using a date type
      let val = props.type === 'date' ? '' : 'pr-10';
      return isError.value
        ? `${val} border-red-300 text-red-900 placeholder-red-300 focus:outline-none focus:ring-red-500 focus:border-red-500`
        : `${val} focus:ring-indigo-500 focus:border-indigo-500 border-gray-300`;
    });

    // The "hint" text will display any necessary hints as well as any error messages.
    // Styling and values of said hint text are primarily based on whether an input is in an error state.
    const hintClass = computed(() =>
      isError.value ? 'text-red-600' : 'text-gray-500'
    );
    const hintId = computed(() =>
      isError.value ? `${props.id}-error` : `${props.id}-input`
    );

    const hintText = computed(() => {
      if (errorText.value.length > 0) return errorText.value;
      if (!!props.hint) return props.hint;
      return '';
    });

    const hasHint = computed(() => !!hintText.value.length);

    return {
      hasHint,
      hintText,
      hintClass,
      hintId,
      dynamicClass,
      isError,
      autofocus: props.autofocus,
      vuelidate: props.vuelidate,
      updateValue,
    };
  },
});
</script>
