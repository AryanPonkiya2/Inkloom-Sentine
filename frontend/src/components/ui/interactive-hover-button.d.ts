import React from "react";

export type ButtonThemeVariant =
  | "default"
  | "primary"
  | "cyan"
  | "emerald"
  | "amber"
  | "crimson"
  | "glass";

export interface InteractiveHoverButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  text?: string;
  variant?: ButtonThemeVariant;
  icon?: React.ReactNode;
}

export declare const InteractiveHoverButton: React.ForwardRefExoticComponent<
  InteractiveHoverButtonProps & React.RefAttributes<HTMLButtonElement>
>;

export declare function InteractiveHoverButtonDemo(): React.JSX.Element;

export default InteractiveHoverButton;

