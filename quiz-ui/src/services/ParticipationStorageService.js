export default {
    clear() {
      window.localStorage.clear();
    },
    savePlayerName(playerName) {
      window.localStorage.setItem("playerName", playerName);
    },
    getPlayerName() {
      return window.localStorage.getItem("playerName");
    },
    saveParticipationScore(participationScore) {
      window.localStorage.setItem("participationScore", participationScore);
    },
    getParticipationScore() {
      return window.localStorage.getItem("participationScore");
    },
    saveAuthToken(token) {
      window.localStorage.setItem("authToken", token);
    },
    getAuthToken() {
      return window.localStorage.getItem("authToken");
    },
    clearAuthToken() {
      window.localStorage.removeItem("authToken");
    }
  };
  