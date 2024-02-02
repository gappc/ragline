import { MaybeRef, computed, toValue } from "vue";
import { Size, Tone, Variant } from "./types";

export const variantClass: Record<Variant, Record<Tone, string>> = {
  solid: {
    primary: "bg-white text-app-border border border-transparent",
    // "bg-white text-app-border border border-transparent hover:bg-inherit hover:text-white hover:border-inherit",
  },
  ghost: {
    primary: "bg-inherit text-white border",
    // "bg-inherit text-white border hover:bg-white hover:text-app-border hover:border-transparent",
  },
};

export const sizeClass: Record<Size, string> = {
  xs: "leading-tight",
  sm: "pt-1.5 pb-1.5 px-6 leading-tight",
  md: "py-[19px] px-9 leading-tight",
};

export const useButtonClasses = ({
  size = "md",
  tone = "primary",
  variant = "solid",
  disabled = false,
}: {
  size: MaybeRef<Size>;
  tone: MaybeRef<Tone>;
  variant: MaybeRef<Variant>;
  disabled: MaybeRef<boolean>;
}) =>
  computed(
    () =>
      // Base classes
      "inline-block transition-colors " +
      // Handle variant and tone
      variantClass[toValue(variant)][toValue(tone)] +
      " " +
      // Handle size
      sizeClass[toValue(size)] +
      // Handle disabled state
      (toValue(disabled) ? " opacity-50" : "")
  );
