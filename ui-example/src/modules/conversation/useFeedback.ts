import { client } from "../api/client";
import { useConversationStore } from "./conversationStore";
import { ConversationItem, Sentiment } from "./types";

export const sendSentiment = async (
  conversationId: string | null,
  promptId: string | null,
  currentItems: ConversationItem[],
  sentiment: Sentiment
) => {
  if (!paramsValid(conversationId, promptId)) {
    return false;
  }

  const item = currentItems.at(-1);

  if (item == null) {
    console.warn("item is undefined");
    return false;
  }

  await send(`/api/sentiment/${conversationId}/${promptId}`, { sentiment });

  if (item.feedback == null) {
    item.feedback = { sentiment, items: [] };
  } else {
    item.feedback.sentiment = sentiment;
  }

  useConversationStore().updateItem(
    conversationId!,
    currentItems.length - 1,
    item
  );

  return true;
};

export const sendFeedback = async (
  conversationId: string | null,
  promptId: string | null,
  currentItems: ConversationItem[],
  feedback: string | null | undefined
) => {
  if (!paramsValid(conversationId, promptId)) {
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

  await send(`/api/feedback/${conversationId}/${promptId}`, { feedback });

  const feedbackItem = { text: feedback, date: new Date() };

  if (item.feedback == null) {
    item.feedback = { sentiment: "none", items: [feedbackItem] };
  } else {
    item.feedback.items = [...item.feedback.items, feedbackItem];
  }

  useConversationStore().updateItem(
    conversationId!,
    currentItems.length - 1,
    item
  );

  return true;
};

const paramsValid = (
  conversationId: string | null,
  promptId: string | null
) => {
  if (conversationId == null) {
    console.warn("conversationId is undefined");
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
