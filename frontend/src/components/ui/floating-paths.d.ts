import React from "react";

export interface FloatingPathsBackgroundProps {
  position?: number;
  className?: string;
  children?: React.ReactNode;
  svgClassName?: string;
  fixed?: boolean;
  variant?: "canvas" | "css";
  opacity?: number;
  style?: React.CSSProperties;
}

export declare function FloatingPathsBackground(
  props: FloatingPathsBackgroundProps
): React.JSX.Element;

export declare function CanvasFloatingPaths(props: {
  position?: number;
  className?: string;
  lineCount?: number;
  speed?: number;
  opacity?: number;
}): React.JSX.Element;

export declare function CssFloatingPaths(props: {
  position?: number;
  className?: string;
  svgClassName?: string;
}): React.JSX.Element;

export declare const FloatingPaths: typeof CanvasFloatingPaths;

export declare function FloatingPathsBackgroundExample(): React.JSX.Element;

export default FloatingPathsBackground;
