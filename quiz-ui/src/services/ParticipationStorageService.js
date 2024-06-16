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
    window.localStorage.setItem("token", token);
  },
  getAuthToken() {
    return window.localStorage.getItem("token");
  },
  clearAuthToken() {
    window.localStorage.removeItem("token");
  }
};
