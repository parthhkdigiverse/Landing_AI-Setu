import { motion } from "framer-motion";
import { Star } from "lucide-react";
import { useEffect, useState } from "react";
import { fetchLandingPageContent, fetchHomeTestimonials } from "@/services/api";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

const TestimonialsSection = () => {
  const navigate = useNavigate();

  const [content, setContent] = useState<any>(null);
  const [livePreview, setLivePreview] = useState<any>(null);
  const [testimonials, setTestimonials] = useState<any[]>([]);

  // 1. Fetch Content & Testimonials
  useEffect(() => {
    const loadData = async () => {
      const data = await fetchLandingPageContent();
      if (data) setContent(data);
      
      const tData = await fetchHomeTestimonials();
      setTestimonials(tData);
    };
    loadData();
  }, []);

  // 2. Live preview listener
  useEffect(() => {
    const handler = (event: any) => {
      if (event.data) {
        setLivePreview((prev: any) => ({ ...prev, ...event.data }));
      }
    };
    window.addEventListener("message", handler);
    return () => window.removeEventListener("message", handler);
  }, []);

  // 3. Duplicate items to create the "Infinite" loop effect
  // We double the array so that as the first set exits, the second set enters seamlessly
  const infiniteTestimonials = [...testimonials, ...testimonials, ...testimonials];

  return (
    <section className="py-16 lg:py-24 bg-background overflow-hidden">
      <div className="container">
        {/* Header Section */}
        <div className="text-center mb-16">
          <span className="text-[#F4B400] font-bold text-sm uppercase tracking-widest">
            {livePreview?.testimonial_label || content?.testimonial_label || "TESTIMONIALS"}
          </span>
          <h2 className="text-3xl lg:text-5xl font-bold mt-3 text-[#1F2E4D]">
            {livePreview?.testimonial_title || content?.testimonial_title || "What Our Customers Say"}
          </h2>
        </div>

        {/* The Infinite Scroll Wrapper */}
        <div className="relative flex overflow-hidden group">
          {/* Left/Right Fades to make it look smooth at the edges */}
          <div className="absolute inset-y-0 left-0 w-32 bg-gradient-to-r from-background to-transparent z-10 pointer-events-none" />
          <div className="absolute inset-y-0 right-0 w-32 bg-gradient-to-l from-background to-transparent z-10 pointer-events-none" />

          {/* This container moves continuously */}
          <div className="flex gap-8 animate-infinite-scroll group-hover:[animation-play-state:paused] py-4">
            {infiniteTestimonials.map((t, i) => (
              <div
                key={i}
                className="w-[350px] flex-shrink-0 bg-white rounded-[2rem] p-8 shadow-[0_10px_40px_-15px_rgba(0,0,0,0.08)] border border-gray-50 whitespace-normal"
              >
                <div className="flex items-center gap-4 mb-6">
                  <div className="w-14 h-14 rounded-full overflow-hidden border-2 border-[#F4B400]/20">
                    <img
                      src={t.image || "/placeholder-user.jpg"}
                      alt={t.name}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div>
                    <p className="font-bold text-lg text-[#1F2E4D]">{t.name}</p>
                    <p className="text-sm text-gray-500">{t.role}</p>
                  </div>
                </div>

                <div className="flex gap-1 mb-4">
                  {Array.from({ length: 5 }).map((_, j) => (
                    <Star key={j} className="h-4 w-4 fill-[#F4B400] text-[#F4B400]" />
                  ))}
                </div>

                <p className="text-gray-600 leading-relaxed italic">
                  "{t.text}"
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* CTA Button */}
        <div className="text-center mt-14">
          <Button
            onClick={() => navigate("/reviews")}
            className="bg-gradient-to-r from-[#F4B400] to-[#E6B800] text-white font-extrabold px-12 py-7 rounded-2xl hover:scale-105 transition-transform shadow-xl shadow-yellow-100"
          >
            {livePreview?.review_button || content?.review_button || "View More Reviews"}
          </Button>
        </div>
      </div>

      {/* Tailwind Extension CSS */}
      <style>{`
        @keyframes infinite-scroll {
          from { transform: translateX(0); }
          to { transform: translateX(calc(-33.33% - 21.3px)); } 
        }
        .animate-infinite-scroll {
          animation: infinite-scroll 40s linear infinite;
        }
      `}</style>
    </section>
  );
};

export default TestimonialsSection;