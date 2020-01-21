<template>
  <div v-if="message" class="error text-danger">
    {{message}}
    <div class="close-button text-danger" @click="hideError">&times;</div>
  </div>
</template>

<script>
export default {
  name: "Error",

  data() {
    return {
      message: null
    };
  },

  methods: {
    showError(receivedMessage) {
      console.log(receivedMessage);
      this.message = receivedMessage;
    },

    hideError() {
      this.message = null;
    }
  }
};
</script>

<style scoped>
.error {
  position: relative;
  bottom: 7%;
  z-index: 1;

  padding: 3px;
  width: 200px;

  background-color: white;
  border: 1px dashed #dc3545;
  border-radius: 10px;
}

.close-button {
  float: right;

  height: 30px;
  line-height: 25px;
  width: 30px;
  text-align: center;

  border: 1.5px solid #dc3545;
  border-radius: 50%;
  background-color: white !important;
}
</style>