import axios from 'redaxios';

class APIClient {
  constructor(endpoints) {
    this.endpoints = endpoints;
  }

  authenticate(participant_id, password) {
    return axios({
      data: {
        participant_id: participant_id,
        password: password
      },
      method: 'POST',
      url: this.endpoints.login
    });
  }

  getFormData() {
    return axios({
      url: this.endpoints.formData,
      withCredentials: true
    })
  }

  logout(csrfToken) {
    return axios({
      headers: {
        'X-CSRF-TOKEN': csrfToken
      },
      method: 'DELETE',
      url: this.endpoints.logout,
      withCredentials: true
    })
  }

  submit(formData, csrfToken) {
    return axios({
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
        'X-CSRF-TOKEN': csrfToken
      },
      method: 'POST',
      url: this.endpoints.submit,
      withCredentials: true
    })
  }
}

export default APIClient;
