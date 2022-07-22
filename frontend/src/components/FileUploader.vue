<script setup>
import axios from "axios";
import { useMemberStore } from "../stores/member";
</script>
<script>
const store = useMemberStore();
export default {
  props: {
    uuid: [String, null],
    accept: [String, null],
  },
  data() {
    return {
      input: null,
      uploaded: false,
      uploading: false,
      uploadProgressPercentage: 0,
      uploadData: null,
    };
  },
  async created() {
    if (this.uuid) {
      console.log("before");
      const response = await axios.get("uploaded-info/" + this.uuid);
      console.log("after");
      console.log("after");
      this.applyUpload(response.data);
    }
  },
  methods: {
    applyUpload(data) {
      this.uploaded = true;
      this.$emit("upload", {
        name: data.name,
        uuid: data.uuid,
      });
    },
    async removeUploaded() {
      this.uploaded = false;
      this.$emit("uploadedRemove");
      await axios.delete(`uploaded/${this.uploadData.uuid}`, {
        headers: {
          Authorization: store.authorizationHeader,
        },
      });
    },
    async submit() {
      this.uploading = true;
      const formData = new FormData();
      formData.append("uploaded", this.input);
      const response = await axios.post("uploaded", formData, {
        headers: {
          Authorization: store.authorizationHeader,
        },
        onUploadProgress: (progressEvent) => {
          this.uploadProgressPercentage = Math.round(
            (progressEvent.loaded / progressEvent.total) * 100
          );
        },
      });
      this.applyUpload(response.data);
      this.uploading = false;
      this.uploaded = true;
      this.uploadData = response.data;
    },
    changeFile(event) {
      const file = event.target.files[0];
      this.input = file;
    },
  },
};
</script>
<template>
  <form @submit.prevent="submit">
    <div class="input-slot">
      <input
        type="file"
        class="form-control"
        @change="changeFile"
        :accept="accept"
        v-if="!uploaded"
        required
      />
      <div
        class="uploaded-name text-primary rounded list-group list-group-flush"
        v-else
      >
        <a
          :href="axios.defaults.baseURL + 'uploaded/' + uploadData.uuid"
          class="list-group-item"
        >
          <small
            ><i
              :class="
                'bi-filetype-' +
                uploadData.name
                  .split('.')
                  [uploadData.name.split('.').length - 1].toLowerCase()
              "
            ></i
            >{{ uploadData.name }}</small
          ></a
        >
      </div>
    </div>
    <div class="feedback">
      <div class="progress" v-if="uploading">
        <div
          class="progress-bar progress-bar-striped progress-bar-animated"
          role="progressbar"
          :style="`width: ${uploadProgressPercentage}%;`"
          aria-valuenow="0"
          aria-valuemin="5"
          aria-valuemax="100"
        ></div>
      </div>
      <button
        type="submit"
        v-if="!uploaded && !uploading"
        class="btn btn-primary"
      >
        올리기
      </button>
      <button
        type="button"
        v-if="uploaded"
        class="btn btn-danger"
        @click="removeUploaded"
      >
        삭제
      </button>
    </div>
  </form>
</template>
<style scoped>
div.uploaded-name {
  height: 100%;
  width: 100%;
  background: white;
}
form {
  display: flex;
  height: 100%;
  align-items: center;
}
.input-slot {
  width: 70%;
  height: 100%;
}
.feedback {
  width: 30%;
  height: 100%;
}
.progress {
  height: 3em;
}
</style>
