import { client } from "../api/client";
import { useChatSessionStore } from "./chatSessionStore";
import { ChatEvent, Sentiment } from "./types";

export const sendSentiment = async (
  chatSessionId: string | null,
  promptId: string | null,
  currentItems: ChatEvent[],
  sentiment: Sentiment
) => {
  if (!paramsValid(chatSessionId, promptId)) {
    return false;
  }

  const item = currentItems.at(-1);

  if (item == null) {
    console.warn("item is undefined");
    return false;
  }

  await send(`/api/sentiment/${chatSessionId}/${promptId}`, { sentiment });

  if (item.feedback == null) {
    item.feedback = { sentiment, items: [] };
  } else {
    item.feedback.sentiment = sentiment;
  }

  useChatSessionStore().updateItem(
    chatSessionId!,
    currentItems.length - 1,
    item
  );

  return true;
};

export const sendFeedback = async (
  chatSessionId: string | null,
  promptId: string | null,
  currentItems: ChatEvent[],
  feedback: string | null | undefined
) => {
  if (!paramsValid(chatSessionId, promptId)) {
    return false;
  }

  if (feedback == null || feedback.trim() === "") {
    console.warn("feedback is empty");
    return false;
  }

  const item = currentItems.at(-1);

  if (item == null) {
    console.warn("item is undefined");
    return false;
  }

  await send(`/api/feedback/${chatSessionId}/${promptId}`, { feedback });

  const feedbackItem = { text: feedback, date: new Date() };

  if (item.feedback == null) {
    item.feedback = { sentiment: "none", items: [feedbackItem] };
  } else {
    item.feedback.items = [...item.feedback.items, feedbackItem];
  }

  useChatSessionStore().updateItem(
    chatSessionId!,
    currentItems.length - 1,
    item
  );

  return true;
};

const paramsValid = (chatSessionId: string | null, promptId: string | null) => {
  if (chatSessionId == null) {
    console.warn("chatSessionId is undefined");
    return false;
  }

  if (promptId == null) {
    console.warn("promptId is undefined");
    return false;
  }

  return true;
};

const send = async (url: string, payload: unknown) => {
  await client(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
};
