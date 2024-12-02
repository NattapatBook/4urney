<template>
  <div :style="{ display: 'flex', alignItems: 'center' }">
    <v-row :style="{ fontWeight: 'bold', fontSize: '1.1em' }">
      <v-col cols="12" :style="{ textAlign: `-webkit-center` }">
        <p class="mb-2">
          <v-icon :style="{ color: `${iconColor}`, fontSize: `${iconSize}` }">{{
            icon
          }}</v-icon>
        </p>
        <p :style="{ fontSize: `${messageSize}`, color: `${textColor}` }">
          {{ message }}
        </p>
        <p
          v-if="subMessage"
          :style="{ fontSize: `${subMessageSize}`, color: `${textColor}` }"
        >
          {{ subMessage }}
        </p>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: "dataError",
  props: {
    icon: {
      default: "mdi-database-off",
      type: String,
    },
    iconColor: {
      default: `#7c7c7c`,
      type: String,
    },
    iconSize: {
      default: ``,
      type: String,
    },
    messageSize: {
      default: `0.8rem`,
      type: String,
    },
    subMessageSize: {
      default: `0.8rem`,
      type: String,
    },
    textColor: {
      default: `#7c7c7c`,
      type: String,
    },
    message: {
      default: "N/A",
      type: String,
    },
    subMessage: {
      default: null,
      type: String,
    },
  },
};
</script>

<style scoped></style>
