export const Page = ({ title, children }: any) => (
  <div className="min-h-screen px-6 py-10">
    <div className="max-w-7xl mx-auto space-y-10">
      <header>
        <h1 className="text-3xl font-semibold tracking-tight">{title}</h1>
        <div className="h-1 w-20 mt-3 rounded-full bg-[#C6A44A]" />
      </header>
      {children}
    </div>
  </div>
);

export const Card = ({ children }: any) => (
  <div className="
    bg-white rounded-2xl p-6
    border border-[#EFE7C9]
    shadow-sm hover:shadow-xl
    transition-all
  ">
    {children}
  </div>
);

export const PrimaryButton = ({ children, ...props }: any) => (
  <button
    {...props}
    className="
      px-6 py-3 rounded-full
      bg-gradient-to-r from-[#C6A44A] to-[#B9983C]
      text-white font-medium tracking-wide
      shadow-lg shadow-[#C6A44A]/20
      hover:scale-[1.02]
      active:scale-[0.98]
      transition
    "
  >
    {children}
  </button>
);

export const Input = (props: any) => (
  <input
    {...props}
    className="
      w-full px-4 py-3 rounded-xl
      bg-white border border-[#EFE7C9]
      focus:ring-2 focus:ring-[#C6A44A]/30
      focus:outline-none transition
    "
  />
);
