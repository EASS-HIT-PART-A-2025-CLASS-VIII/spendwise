import React from 'react';

export const Logo: React.FC = () => {
  return (
    <div className="flex items-center gap-3 py-2">
      <svg
        className="w-12 h-12 shrink-0"
        viewBox="0 0 80 80"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* The Hexagon - Now with 'animate-pulse' for a slow glow effect */}
        <path
          id="hexagonPath"
          d="M40 15 L62 27 L62 53 L40 65 L18 53 L18 27 Z"
          className="stroke-[#238636] fill-[#238636]/10 animate-pulse"
          strokeWidth="6"
          strokeLinejoin="round"
        />
        <g>
          {/* The orbiting spark */}
          <rect x="-4" y="-4" width="8" height="8" fill="white" transform="rotate(45)">
            <animateMotion
              dur="6s"
              repeatCount="indefinite"
              path="M40 15 L62 27 L62 53 L40 65 L18 53 L18 27 Z"
            />
          </rect>

          {/* The blue aura following the spark */}
          <circle r="6" fill="#58a6ff" className="opacity-60 blur-[3px]">
            <animateMotion
              dur="6s"
              repeatCount="indefinite"
              path="M40 15 L62 27 L62 53 L40 65 L18 53 L18 27 Z"
            />
          </circle>
        </g>
      </svg>

      <span className="text-2xl font-black text-white tracking-tighter">
        Spend<span className="text-[#58a6ff]">Wise</span>
      </span>
    </div>
  );
};
