<template>
  <div>
    <v-row :style="{ height: `100%`, alignItems: `center` }">
      <v-col cols="12" :style="{ textAlign: `-webkit-center` }">
        <v-progress-circular
          class="mb-3"
          :size="70"
          :width="7"
          color="rgb(254,56,147)"
          indeterminate
        ></v-progress-circular>
        <p :style="{ color: `${messageColor}` }">{{ message }}</p>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: "LoadingComponent",
  props: {
    message: {
      default: "",
      type: String,
    },
    messageColor: {
      default: `rgb(254,56,147)`,
      type: String,
    },
  },
};
</script>

<style scoped></style>
