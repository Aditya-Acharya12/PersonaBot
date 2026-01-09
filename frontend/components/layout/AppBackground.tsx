"use client";

export default function AppBackground() {
  return (
    <div
      aria-hidden
      className="fixed inset-0 -z-10 overflow-hidden"
    >
      {/* base */}
      <div className="absolute inset-0 bg-background" />

      {/* soft blue glow */}
      <div className="absolute -top-40 left-1/2 -translate-x-1/2 w-[900px] h-[900px] rounded-full bg-blue-500/20 blur-[160px]" />

      {/* secondary glow */}
      <div className="absolute top-[40%] right-[-200px] w-[700px] h-[700px] rounded-full bg-cyan-400/15 blur-[160px]" />
    </div>
  );
}
