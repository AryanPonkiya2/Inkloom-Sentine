import React from "react";
import { ArrowRight } from "lucide-react";
import { cn } from "@/lib/utils";

const THEME_VARIANTS = {
  default: {
    button:
      "border-slate-700/80 bg-gradient-to-b from-[#151c2c] to-[#0d121e] text-slate-100 hover:border-indigo-400/80 shadow-[0_2px_8px_rgba(0,0,0,0.35),inset_0_1px_0_rgba(255,255,255,0.06)]",
    dot: "bg-indigo-400 shadow-[0_0_8px_rgba(99,102,241,0.9)]",
    hoverBg: "bg-gradient-to-r from-indigo-600 to-indigo-700",
    revealed: "text-white font-semibold",
  },
  primary: {
    button:
      "border-indigo-500/60 bg-gradient-to-b from-[#181a38] to-[#0c0d1e] text-indigo-100 hover:border-indigo-400 hover:text-white shadow-[0_2px_12px_rgba(99,102,241,0.25),inset_0_1px_0_rgba(255,255,255,0.08)]",
    dot: "bg-indigo-400 shadow-[0_0_10px_rgba(99,102,241,0.95)]",
    hoverBg: "bg-gradient-to-r from-indigo-600 to-violet-600",
    revealed: "text-white font-bold",
  },
  cyan: {
    button:
      "border-cyan-500/60 bg-gradient-to-b from-[#0e2130] to-[#07131d] text-cyan-100 hover:border-cyan-400 hover:text-white shadow-[0_2px_12px_rgba(6,182,212,0.25),inset_0_1px_0_rgba(255,255,255,0.08)]",
    dot: "bg-cyan-400 shadow-[0_0_10px_rgba(6,182,212,0.95)]",
    hoverBg: "bg-gradient-to-r from-cyan-600 to-blue-600",
    revealed: "text-white font-bold",
  },
  emerald: {
    button:
      "border-emerald-500/60 bg-gradient-to-b from-[#0c241c] to-[#06140e] text-emerald-100 hover:border-emerald-400 hover:text-white shadow-[0_2px_12px_rgba(16,185,129,0.25),inset_0_1px_0_rgba(255,255,255,0.08)]",
    dot: "bg-emerald-400 shadow-[0_0_10px_rgba(16,185,129,0.95)]",
    hoverBg: "bg-gradient-to-r from-emerald-600 to-teal-600",
    revealed: "text-white font-bold",
  },
  amber: {
    button:
      "border-amber-500/60 bg-gradient-to-b from-[#241a0c] to-[#140e06] text-amber-100 hover:border-amber-400 hover:text-white shadow-[0_2px_12px_rgba(245,158,11,0.25),inset_0_1px_0_rgba(255,255,255,0.08)]",
    dot: "bg-amber-400 shadow-[0_0_10px_rgba(245,158,11,0.95)]",
    hoverBg: "bg-gradient-to-r from-amber-500 to-amber-600",
    revealed: "text-slate-950 font-bold",
  },
  crimson: {
    button:
      "border-rose-500/60 bg-gradient-to-b from-[#260e18] to-[#14060c] text-rose-100 hover:border-rose-400 hover:text-white shadow-[0_2px_12px_rgba(244,63,94,0.25),inset_0_1px_0_rgba(255,255,255,0.08)]",
    dot: "bg-rose-500 shadow-[0_0_10px_rgba(244,63,94,0.95)]",
    hoverBg: "bg-gradient-to-r from-rose-600 to-rose-700",
    revealed: "text-white font-bold",
  },
  glass: {
    button:
      "border-slate-700/80 bg-gradient-to-b from-slate-800/50 to-slate-900/60 text-slate-200 hover:border-slate-500 hover:text-white shadow-[0_2px_8px_rgba(0,0,0,0.3),inset_0_1px_0_rgba(255,255,255,0.05)]",
    dot: "bg-slate-400 shadow-[0_0_6px_rgba(148,163,184,0.6)]",
    hoverBg: "bg-slate-700",
    revealed: "text-white font-medium",
  },
};

const SIZE_VARIANTS = {
  sm: "min-h-[34px] px-3.5 py-1.5 text-[11px]",
  md: "min-h-[42px] px-5 py-2.5 text-xs",
  lg: "min-h-[46px] px-6 py-3 text-sm",
};

const InteractiveHoverButton = React.forwardRef(
  (
    {
      text = "Button",
      children,
      className,
      variant = "default",
      size = "md",
      icon,
      disabled = false,
      showDot = true,
      ...props
    },
    ref
  ) => {
    const label = children || text;
    const theme = THEME_VARIANTS[variant] || THEME_VARIANTS.default;
    const sizeClass = SIZE_VARIANTS[size] || SIZE_VARIANTS.md;
    const IconComponent = icon || <ArrowRight className="h-3.5 w-3.5 shrink-0" />;

    return (
      <button
        ref={ref}
        disabled={disabled}
        className={cn(
          "group relative inline-flex items-center justify-center cursor-pointer overflow-hidden rounded-lg border font-semibold tracking-wide whitespace-nowrap transition-all duration-300 select-none",
          sizeClass,
          theme.button,
          disabled && "cursor-not-allowed opacity-50 hover:border-transparent",
          className
        )}
        {...props}
      >
        {/* Expanding Background Aura on Hover (Sweeps smoothly within rectangular bounds) */}
        <div
          className={cn(
            "pointer-events-none absolute -left-4 top-1/2 -translate-y-1/2 h-8 w-8 scale-0 rounded-full opacity-0 transition-transform duration-500 ease-out group-hover:scale-[32] group-hover:opacity-100",
            theme.hoverBg || theme.dot
          )}
        />

        {/* Initial Static View with Cleanly-Aligned Dot & Text (Never overlaps letters) */}
        <span className="relative z-10 inline-flex items-center justify-center gap-2.5 transition-all duration-300 group-hover:translate-x-6 group-hover:opacity-0">
          {showDot && (
            <span
              className={cn(
                "h-2 w-2 rounded-sm shrink-0 transition-transform duration-300 group-hover:scale-0",
                theme.dot
              )}
            />
          )}
          <span className="leading-none whitespace-nowrap">{label}</span>
        </span>

        {/* Revealed Hover View with Sliding Icon & Action Text */}
        <div
          className={cn(
            "absolute inset-0 z-20 flex h-full w-full -translate-x-6 items-center justify-center gap-2 px-3 opacity-0 transition-all duration-300 group-hover:translate-x-0 group-hover:opacity-100",
            theme.revealed
          )}
        >
          <span className="leading-none whitespace-nowrap">{label}</span>
          {IconComponent}
        </div>
      </button>
    );
  }
);

InteractiveHoverButton.displayName = "InteractiveHoverButton";

// Demo component as referenced in prompt
function InteractiveHoverButtonDemo() {
  return (
    <div className="relative flex flex-wrap items-center justify-center gap-4 p-4">
      <InteractiveHoverButton text="Primary Indigo" variant="primary" size="md" />
      <InteractiveHoverButton text="Cyan Cyber" variant="cyan" size="md" />
      <InteractiveHoverButton text="Emerald Glow" variant="emerald" size="md" />
      <InteractiveHoverButton text="Amber Review" variant="amber" size="md" />
      <InteractiveHoverButton text="Crimson Alert" variant="crimson" size="md" />
      <InteractiveHoverButton text="Glass Secondary" variant="glass" size="md" />
    </div>
  );
}

export { InteractiveHoverButton, InteractiveHoverButtonDemo };
export default InteractiveHoverButton;
