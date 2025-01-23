<template>
  <v-dialog v-model="internalModel" width="500">
    <v-card class="rounded-xl">
      <!-- Dialog Title -->
      <v-card-text
        class="mt-2 pb-0"
        :style="{ fontWeight: `bold`, fontSize: `1.2rem` }"
      >
        Knowledge Upload
      </v-card-text>

      <v-card-text class="pb-0">
        <div>
          <span> Choose a file to import your knowledge base. </span>
        </div>
      </v-card-text>
      <v-card-text v-if="isLoading" :style="{ height: `156px` }">
        <Loading :message="`Uploading...`" />
      </v-card-text>
      <!-- Dialog Content -->
      <v-card-text v-else :style="{ height: `156px` }">
        <div class="file-upload">
          <div
            :style="{
              display: `flex`,
              alignItems: `center`,
            }"
          >
            <v-icon
              class="mr-2"
              :color="
                !fileRequiredRule(selectedFile) && selectedFile
                  ? `red`
                  : fileRequiredRule(selectedFile)
                  ? `primary`
                  : ``
              "
              :style="{ fontSize: `2rem` }"
            >
              {{
                !fileRequiredRule(selectedFile) && selectedFile
                  ? `mdi-close`
                  : fileRequiredRule(selectedFile)
                  ? `mdi-file`
                  : `mdi-paperclip`
              }}
            </v-icon>
            <v-file-input
              hide-details
              rounded
              :color="
                !fileRequiredRule(selectedFile) && selectedFile
                  ? `red`
                  : fileRequiredRule(selectedFile)
                  ? `primary`
                  : ``
              "
              :base-color="
                !fileRequiredRule(selectedFile) && selectedFile
                  ? `red`
                  : fileRequiredRule(selectedFile)
                  ? `primary`
                  : ``
              "
              v-model="selectedFile"
              :accept="acceptedFormats"
              label="Choose file"
              clearable
              variant="outlined"
              prepend-icon=""
              dense
              chips
            />
          </div>
          <p
            v-if="fileRequiredRule(selectedFile)"
            :style="{ textAlign: `end`, fontSize: `0.8rem`, color: `#1867c0` }"
            class="pr-2"
          >
            File Size: {{ formatFileSize(selectedFile.size) }}
          </p>
          <p
            class="pr-2"
            v-else
            :style="{
              textAlign: `end`,
              fontSize: `0.8rem`,
              color:
                !fileRequiredRule(selectedFile) && selectedFile ? `red` : ``,
            }"
          >
            CSV, PDF, XLSX format only
          </p>
        </div>
      </v-card-text>

      <!-- Dialog Actions -->
      <v-card-text
        class="pt-0"
        :style="{
          display: 'flex',
          flexDirection: 'row',
          alignItems: 'center',
          justifyContent: 'flex-end',
        }"
      >
        <v-btn :disabled="isLoading" @click="closeDialog" variant="text">
          Cancel
        </v-btn>
        <v-btn
          @click="uploadFile"
          :disabled="!fileRequiredRule(selectedFile) || isLoading"
          color="primary"
          class="ml-2"
          text
        >
          Upload File
        </v-btn>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from "axios";
import Loading from "../tools/loading.vue";

export default {
  name: "FileUploadDialog",
  components: { Loading },
  props: {
    modelValue: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      acceptedFormats: ".xlsx,.csv,.pdf",
      selectedFile: null,
      isLoading: false,
    };
  },
  computed: {
    internalModel: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },
  },
  methods: {
    closeDialog() {
      this.resetFileInput();
      this.internalModel = false;
    },
    fileRequiredRule(file) {
      if (!file) {
        return false;
      }
      const allowedExtensions = ["xlsx", "csv", "pdf"];
      const fileExtension = file.name.split(".").pop().toLowerCase();

      if (!allowedExtensions.includes(fileExtension)) {
        return false;
      }

      return true;
    },
    formatFileSize(sizeInBytes) {
      if (sizeInBytes < 1024) {
        return `${sizeInBytes} B`; // Bytes
      } else if (sizeInBytes < 1048576) {
        return `${(sizeInBytes / 1024).toFixed(2)} KB`; // Kilobytes
      } else if (sizeInBytes < 1073741824) {
        return `${(sizeInBytes / 1048576).toFixed(2)} MB`; // Megabytes
      } else {
        return `${(sizeInBytes / 1073741824).toFixed(2)} GB`; // Gigabytes
      }
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        // Check file extension
        const validExtensions = ["xlsx", "csv", "pdf"];
        const fileExtension = file.name.split(".").pop().toLowerCase();

        if (validExtensions.includes(fileExtension)) {
          this.selectedFile = file;
        } else {
          alert("Please select a valid file (xlsx, csv, pdf).");
          this.resetFileInput();
        }
      }
    },
    resetFileInput() {
      this.selectedFile = null;
    },
    async uploadFile() {
      this.isLoading = true;
      if (this.selectedFile) {
        const formData = new FormData();
        formData.append("file", this.selectedFile);

        // console.log(this.selectedFile.name);
        try {
          const response = await axios.post("api/chat_center/uploadTest/", {
            file: this.selectedFile.name,
          });

          if (response.status === 200) {
            this.uploadS3(response.data);
          } else {
            this.snackbarCallback(`Upload failed`, false, true);
            this.isLoading = false;
          }
        } catch (error) {
          this.snackbarCallback(error, false, true);
          this.isLoading = false;
        }
      }
    },
    async uploadS3(item) {
      const formData = new FormData();
      for (const key in item.fields) {
        formData.append(key, item.fields[key]);
      }
      formData.append("file", this.selectedFile);
      try {
        const response = await axios.post(`${item.url}`, formData);
        console.log(response.status, response.status === 204);
        if (response.status === 204) {
          this.snackbarCallback(
            `Success! Your file has been uploaded.`,
            true,
            true
          );
          this.isLoading = false;
          this.resetFileInput();
          // this.closeDialog();
        } else {
          this.snackbarCallback(`Upload failed`, false, true);
          this.isLoading = false;
        }
      } catch (error) {
        this.snackbarCallback(error, false, true);
        this.isLoading = false;
      }
    },
    snackbarCallback(snackbarMsg, snackbarSuccess, snackbarAlert) {
      this.$emit("snackbar", {
        snackbarMsg,
        snackbarSuccess,
        snackbarAlert,
      });
    },
  },
};
</script>

<style scoped>
.file-upload {
  margin: 20px;
}

.upload-label {
  display: block;
  margin-bottom: 10px;
  font-weight: bold;
}

input[type="file"] {
  margin-bottom: 10px;
  display: block;
}

.file-info {
  margin-top: 10px;
  font-size: 14px;
}

.v-btn {
  font-weight: 600;
}
</style>
