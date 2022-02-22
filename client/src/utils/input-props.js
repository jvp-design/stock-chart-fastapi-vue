// input-props.js

export default {
  id: {
    type: String,
    required: true,
  },
  modelValue: {
    type: String,
    required: true
  },
  label: {
    type: String,
    required: true,
  },
  hint: {
    type: String,
    required: false,
    default: '',
  },
};
