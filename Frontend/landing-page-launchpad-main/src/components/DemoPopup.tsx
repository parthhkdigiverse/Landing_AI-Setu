import { useEffect, useState } from "react";
import DemoForm from "@/components/DemoForm";

const DemoPopup = () => {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    console.log("DemoPopup mounted");

    const timer = setTimeout(() => {
      console.log("Opening popup");
      setOpen(true);
    }, 90000); 

    return () => clearTimeout(timer);
  }, []);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/50">
      <div className="bg-white p-6 rounded-lg w-[400px] relative">

        <button
          onClick={() => setOpen(false)}
          className="absolute top-2 right-3 text-xl"
        >
          ×
        </button>

        <h2 className="text-xl font-bold mb-4 text-center">
          Book Free Demo
        </h2>

        <DemoForm />

      </div>
    </div>
  );
};

export default DemoPopup;