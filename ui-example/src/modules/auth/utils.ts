export const buildBasicAuthHeader = (
  username: string,
  token: string
): Record<string, string> => ({
  Authorization: "Basic " + btoa(`${username}:${token}`),
});
