export class ResponseError extends Error {
  readonly status: number;
  readonly statusText: string;
  readonly message: string;

  private constructor(status: number, statusText: string, message: string) {
    super(statusText);
    this.status = status;
    this.statusText = statusText;
    this.message = message;
  }

  public static fromResponse = async (
    response: Response
  ): Promise<ResponseError> => {
    const status = response.status;
    const statusText = response.statusText;
    const message = await this.parseMessage(response);
    console.log("Error:", response);

    return new ResponseError(status, statusText, message);
  };

  private static parseMessage = async (response: Response): Promise<string> => {
    const contentType = response.headers.get("Content-Type");

    const isJson =
      contentType != null && contentType.indexOf("application/json") !== -1;
    if (isJson) {
      const json = await response.json();
      const message =
        json != null && json.detail != null
          ? json.detail
          : JSON.stringify(json);
      return message;
    }
    return await response.text();
  };
}

export const errorToMessage = (error: unknown): string => {
  if (error instanceof ResponseError) {
    if (error.message.length > 0) {
      return error.message;
    }
    return `(${error.status}) ${error.statusText}`;
  }

  return error instanceof Error ? error.message : JSON.stringify(error);
};
