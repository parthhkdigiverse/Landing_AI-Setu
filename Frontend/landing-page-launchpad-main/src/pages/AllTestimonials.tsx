import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { motion } from "framer-motion";
import { Star } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchLandingPageContent, fetchAllTestimonials } from "@/services/api";
import { fetchLandingPageContent } from "@/services/api";

const AllTestimonials = () => {
  const [reviews, setReviews] = useState<any[]>([]);
  const [content, setContent] = useState<any>(null);
  const [livePreview, setLivePreview] = useState<any>(null);

  // 1. Fetch Content (for Title/Desc) & All Testimonials
  useEffect(() => {
  const interval = setInterval(async () => {
    const res = await fetch("http://127.0.0.1:8000/api/landing-page/");
    const data = await res.json();
    setContent(data);
  }, 5000); // fetch every 5 seconds
  return () => clearInterval(interval);
}, []);

  // 2. Listen for live preview messages (admin updates)
  useEffect(() => {
    const handler = (event: MessageEvent) => {
      if (event.data && typeof event.data === "object") {
        setLivePreview((prev: any) => ({ ...prev, ...event.data }));
      }
    };
    window.addEventListener("message", handler);
    return () => window.removeEventListener("message", handler);
  }, []);

  useEffect(() => {
    const loadReviews = async () => {
      const data = await fetchAllTestimonials();
      setReviews(data);
    };
    loadReviews();
  }, []);

  return (
    <>
      <Header />

      <main className="bg-[#F5F6FA] min-h-screen">
        {/* HERO SECTION */}
        <section className="bg-gradient-to-br from-[#1F2E4D] to-[#2E4573] text-white py-24">
          <div className="max-w-6xl mx-auto px-6 text-center">
            
            {/* Breadcrumb */}
            <div className="mb-6 text-sm text-gray-300">
              <Link to="/" className="hover:text-[#F4B400] transition">Home</Link>
              <span className="mx-2">/</span>
              <span className="text-white">Reviews</span>
            </div>

            {/* Title - Previewable */}
            <motion.h1
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="text-4xl md:text-6xl font-bold mb-6"
            >
              {livePreview?.all_reviews_title || content?.all_reviews_title || "Customer Reviews"}
            </motion.h1>

            {/* Subtitle - Previewable */}
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.8 }}
              className="max-w-3xl mx-auto text-gray-200 text-lg md:text-xl leading-relaxed"
            >
              {livePreview?.all_reviews_desc || content?.all_reviews_desc || "See what retailers across India are saying about AI-Setu ERP."}
            </motion.p>
          </div>
        </section>

        {/* REVIEWS GRID SECTION */}
        <section className="py-20">
          <div className="max-w-7xl mx-auto px-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {reviews.map((review, i) => (
                <motion.div
                  key={review.id || i}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.05 }}
                  className="bg-white rounded-[2rem] p-8 shadow-[0_10px_40px_-15px_rgba(0,0,0,0.08)] border border-gray-50 flex flex-col justify-between hover:shadow-xl transition-shadow duration-300"
                >
                  <div>
                    {/* User Info */}
                    <div className="flex items-center gap-4 mb-6">
                      <div className="w-14 h-14 rounded-full overflow-hidden border-2 border-[#F4B400]/20 shadow-sm">
                        <img
                          src={review.image || "/placeholder-user.jpg"}
                          alt={review.name}
                          className="w-full h-full object-cover"
                        />
                      </div>
                      <div>
                        <p className="font-bold text-lg text-[#1F2E4D]">{review.name}</p>
                        <p className="text-sm text-gray-500 font-medium">{review.role}</p>
                      </div>
                    </div>

                    {/* Rating */}
                    <div className="flex gap-1 mb-4">
                      {Array.from({ length: 5 }).map((_, j) => (
                        <Star 
                          key={j} 
                          className={`h-4 w-4 ${j < review.rating ? "fill-[#F4B400] text-[#F4B400]" : "text-gray-200"}`} 
                        />
                      ))}
                    </div>

                    {/* Review Text */}
                    <p className="text-gray-600 leading-relaxed italic mb-4">
                      "{review.text}"
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </>
  );
};

export default AllTestimonials;