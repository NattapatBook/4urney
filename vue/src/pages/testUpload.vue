<template>
  <div class="mt-16 pt-16">
    <div class="file-upload">
      <label for="file-upload" class="upload-label">
        Select a file (xlsx, csv, pdf)
      </label>
      <input
        id="file-upload"
        type="file"
        @change="handleFileUpload"
        :accept="acceptedFormats"
      />
      <div v-if="selectedFile" class="file-info">
        <p>File Name: {{ selectedFile.name }}</p>
        <p>File Size: {{ (selectedFile.size / 1024).toFixed(2) }} KB</p>
      </div>
      <button v-if="selectedFile" @click="uploadFile">Upload File</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      acceptedFormats: ".xlsx,.csv,.pdf", // Allowed file extensions
      selectedFile: null, // Holds the uploaded file
    };
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        // Check file extension
        const validExtensions = ["xlsx", "csv", "pdf"];
        const fileExtension = file.name.split(".").pop().toLowerCase();

        if (validExtensions.includes(fileExtension)) {
          this.selectedFile = file;
        } else {
          alert("Please select a file with extension xlsx, csv, or pdf.");
          this.resetFileInput();
        }
      }
    },
    resetFileInput() {
      this.selectedFile = null;
      document.getElementById("file-upload").value = "";
    },
    async uploadFile() {
      console.log(`FILE ==>`, this.selectedFile);
      if (this.selectedFile) {
        const formData = new FormData();
        formData.append("file", this.selectedFile);

        try {
          const response = await axios.post(
            "api/chat_center/uploadTest/",
            formData,
            {
              headers: {
                "Content-Type": "multipart/form-data", // Specify content type
              },
            }
          );

          if (response.status === 200) {
            alert("File uploaded successfully!");
            this.resetFileInput();
          } else {
            alert("An error occurred during the file upload.");
          }
        } catch (error) {
          console.error("Error uploading file:", error);
          alert("An error occurred during the file upload.");
        }
      }
    },
  },
};
</script>

<style>
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
}

.file-info {
  margin-top: 10px;
  font-size: 14px;
}

button {
  background-color: #007bff;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
