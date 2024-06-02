import axios from "axios";

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
});

export default {
  async call(method, resource, data = null, token = null) {
    const headers = {
      "Content-Type": "application/json",
    };
    if (token != null) {
      headers.authorization = "Bearer " + token;
    }

    try {
      const response = await instance({
        method,
        headers: headers,
        url: resource,
        data,
      });
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  },
  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  getQuizQuestions() {
    return this.call("get", "quiz-questions");
  },
};
