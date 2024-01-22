import { useAuthStore } from "../auth/authStore";
import { ResponseError } from "./responseError";

export const client = async (
  input: RequestInfo | URL,
  init?: RequestInit
): Promise<Response> => {
  const authHeader = useAuthStore().basicAuthHeader;

  const response = await fetch(input, {
    ...init,
    headers: { ...authHeader, ...init?.headers },
  });

  if (response.status >= 400) {
    console.log("Error:", response);
    throw await ResponseError.fromResponse(response);
  }

  return response;
};

export async function* parseEventStream(response: Response) {
  const reader = response.body?.getReader();
  const decoder = new TextDecoder("utf-8");
  while (true) {
    const { value, done } = await reader!.read();
    if (done) {
      break;
    }
    const decodedValue = decoder.decode(value);
    yield decodedValue;
  }
}
