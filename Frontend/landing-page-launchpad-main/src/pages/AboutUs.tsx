import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { motion } from "framer-motion";
import { useRef, useState, useEffect } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";

import DemoForm from "@/components/DemoForm";

// IMPORT API SERVICES
import { fetchAboutPageContent, AboutPageContent } from "@/services/api";

// IMPORT IMAGES FROM src/static/assets
import kiranaImg from "@/assets/kirana.jpg";
import generalImg from "@/assets/general.jpg";
import medicalImg from "@/assets/medical.jpg";
import hardwareImg from "@/assets/hardware.jpg";
import marginImg from "@/assets/margin.jpg";
import erpDevicesImg from "@/assets/erp-devices.jpg";

const AboutUs = () => {
  const [demoOpen, setDemoOpen] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  // --- LIVE PREVIEW & DATA STATE ---
  const [content, setContent] = useState<AboutPageContent | null>(null);

  // 1. Load data from the database on initial page load
  useEffect(() => {
    const loadData = async () => {
      // Adding a timestamp ensures the browser doesn't serve a cached version
      const data = await fetchAboutPageContent(); 
      if (data) {
        setContent(data);
      }
    };

    loadData();

    // Also listen for the 'reload' signal from the Admin Save button
    const handleSaveRefresh = (event: MessageEvent) => {
      if (event.data === "reload_full_data") {
        loadData();
      }
    };

    window.addEventListener("message", handleSaveRefresh);
    return () => window.removeEventListener("message", handleSaveRefresh);
  }, []);

  // 2. Listen for "postMessage" from Django Admin for the Live Preview effect
  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      // If we receive data from the admin iframe, update the UI immediately
      if (event.data && typeof event.data === 'object') {
        setContent((prev) => ({
          ...prev,
          ...event.data,
        } as AboutPageContent));
      }
    };

    window.addEventListener("message", handleMessage);
    return () => window.removeEventListener("message", handleMessage);
  }, []);

  const scroll = (direction: "left" | "right") => {
    if (!scrollRef.current) return;
    const scrollAmount = 350;
    scrollRef.current.scrollBy({
      left: direction === "left" ? -scrollAmount : scrollAmount,
      behavior: "smooth",
    });
  };

  // Maps the "Serve" section titles to the state, with your original text as fallback
  const stores = [
    { title: content?.serve1_title || "Kirana Store", image: kiranaImg },
    { title: content?.serve2_title || "General Store", image: generalImg },
    { title: content?.serve3_title || "Medical Store", image: medicalImg },
    { title: content?.serve4_title || "Hardware Store", image: hardwareImg },
    { title: "Margin Business Retailers", image: marginImg },
  ];

  return (
    <>
      <Header />

      <main className="bg-[#F5F6FA]">
        {/* HERO SECTION */}
        <section className="bg-gradient-to-br from-[#1F2E4D] to-[#2E4573] text-white py-24">
          <div className="max-w-6xl mx-auto px-6 text-center">
            <motion.h1
              initial={{ opacity: 0, y: -60, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.9, ease: "easeOut" }}
              className="text-5xl font-bold mb-6"
            >
              {content?.hero_title || "About AI-Setu ERP"}
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4, duration: 1, ease: "easeOut" }}
              className="max-w-3xl mx-auto text-gray-200 text-lg"
            >
              {content?.hero_description || "AI-Setu ERP empowers retailers with modern technology to simplify store management. We help SMEs automate operations, improve efficiency, and grow faster with intelligent ERP solutions."}
            </motion.p>
          </div>
        </section>

        {/* ABOUT INTRO SECTION */}
        <section className="py-24 bg-white">
          <div className="max-w-7xl mx-auto px-6 grid md:grid-cols-2 gap-16 items-center">
            {/* LEFT TEXT CONTENT */}
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              viewport={{ once: true }}
            >
              <h2 className="text-[#3BA6E3] font-bold text-xl mb-4">
                {content?.about_label || "ABOUT US"}
              </h2>
              <h3 className="text-3xl font-bold text-gray-800 mb-6 leading-snug">
                {content?.about_heading || "WE ARE ON A DRIVE TO MAKE THE RETAIL INDUSTRY MORE EFFICIENT."}
              </h3>
              <p className="text-gray-600 mb-4">
                {content?.about_description_1 || (
                  <><strong>AI-Setu ERP</strong> is the future of retail. From empowering diverse industries to leveraging their true potential with features like Smart Retail, Omni-Channel management, and Hybrid-POS.</>
                )}
              </p>
              <p className="text-gray-600 mb-4">
                {content?.about_description_2 || "SMEs often struggle to find a comprehensive cloud-based ERP and POS solution that can scale with their growth."}
              </p>
              <p className="text-gray-600 mb-6">
                {content?.about_description_3 || (
                  <><strong>AI-Setu ERP empowers SMEs</strong> to use modern ERP tools without complexity and grow their businesses with automation and analytics.</>
                )}
              </p>
            </motion.div>

            {/* RIGHT IMAGE WITH FLOAT MOTION */}
            <motion.div
              initial={{ opacity: 0, x: 50, scale: 0.9 }}
              whileInView={{ opacity: 1, x: 0, scale: 1 }}
              transition={{ duration: 1, ease: "easeOut" }}
              viewport={{ once: true }}
            >
              <motion.img
                src={erpDevicesImg}
                alt="AI Setu ERP Dashboard"
                className="w-full rounded-xl shadow-lg object-cover"
                animate={{ y: [0, -8, 0] }}
                transition={{
                  y: { duration: 6, repeat: Infinity, ease: "easeInOut" },
                }}
              />
            </motion.div>
          </div>
        </section>

        {/* MISSION SECTION */}
        <section className="py-24">
          <div className="max-w-6xl mx-auto px-6 grid md:grid-cols-2 gap-16 items-center">
            <motion.div
              initial={{ opacity: 0, x: -80, rotate: -3, scale: 0.95 }}
              whileInView={{ opacity: 1, x: 0, rotate: 0, scale: 1 }}
              transition={{ duration: 0.9, ease: "easeOut" }}
              viewport={{ once: true }}
            >
              <h2 className="text-4xl font-bold text-[#1F2E4D] mb-6">
                {content?.mission_title || "Our Mission"}
              </h2>
              <p className="text-gray-600 mb-6">
                {content?.mission_description || "Retail businesses are the backbone of the Indian economy, yet many rely on outdated tools. AI-Setu ERP brings modern technology to retail businesses, enabling inventory tracking, billing, sales analysis, and smarter decisions with ease."}
              </p>
            </motion.div>

            {/* WHY CHOOSE US CARD */}
            <motion.div
              initial={{ opacity: 0, y: 40, scale: 0.9 }}
              whileInView={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 1, ease: "anticipate" }}
              viewport={{ once: true }}
              className="bg-white p-10 rounded-xl shadow-lg"
            >
              <h3 className="text-2xl font-semibold text-[#1F2E4D] mb-4">
                {content?.why_choose_title || "Why Choose AI-Setu ERP?"}
              </h3>
              <ul className="space-y-3 text-gray-600">
                <li>✔ {content?.why_point_1 || "Smart AI-powered insights"}</li>
                <li>✔ {content?.why_point_2 || "Fast and reliable billing"}</li>
                <li>✔ {content?.why_point_3 || "Real-time inventory tracking"}</li>
                <li>✔ {content?.why_point_4 || "Powerful sales analytics"}</li>
                <li>✔ {content?.why_point_5 || "Built specifically for Indian retailers"}</li>
              </ul>
            </motion.div>
          </div>
        </section>

        {/* WHO WE SERVE SECTION */}
        <section className="py-24 bg-[#F5F6FA]">
          <div className="max-w-7xl mx-auto px-6">
            <div className="text-center mb-14">
              <h2 className="text-4xl font-bold text-[#1F2E4D]">
                {content?.serve_title || "WHOM DO WE"} <span className="text-[#F4B400]">SERVE?</span>
              </h2>
              <p className="text-gray-600 mt-4 max-w-2xl mx-auto">
                {content?.serve_subtitle || "We serve all types of retail businesses with our ERP solutions."}
              </p>
            </div>

            <div className="relative">
              {/* Carousel Navigation */}
              <button onClick={() => scroll("left")} className="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-white shadow-md p-3 rounded-full hover:bg-[#F4B400] transition">
                <ChevronLeft />
              </button>
              <button onClick={() => scroll("right")} className="absolute right-0 top-1/2 -translate-y-1/2 z-10 bg-white shadow-md p-3 rounded-full hover:bg-[#F4B400] transition">
                <ChevronRight />
              </button>

              {/* Stores Carousel */}
              <div ref={scrollRef} className="flex gap-8 overflow-x-auto scroll-smooth no-scrollbar px-4">
                {stores.map((store, index) => (
                  <motion.div
                    key={index}
                    whileHover={{ scale: 1.05 }}
                    className="min-w-[300px] h-[240px] rounded-xl overflow-hidden shadow-lg relative cursor-pointer"
                  >
                    <img src={store.image} alt={store.title} className="w-full h-full object-cover" />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/30 to-transparent"></div>
                    <div className="absolute bottom-5 left-5 text-white text-lg font-semibold tracking-wide">
                      {store.title.toUpperCase()}
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* CALL TO ACTION SECTION */}
        <section className="py-24 bg-[#1F2E4D] text-white text-center">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="max-w-4xl mx-auto px-6"
          >
            <h2 className="text-4xl font-bold mb-6">
              {content?.cta_title || "Transform Your Retail Business"}
            </h2>
            <p className="text-gray-300 mb-8">
              {content?.cta_description || "Join retailers who are already using AI-Setu ERP to streamline operations."}
            </p>

            <Button
              onClick={() => setDemoOpen(true)}
              className="bg-gold-gradient text-accent-foreground font-bold text-base px-8 py-6 transition-all duration-200 shadow-lg hover:scale-105 active:scale-95 animate-pulse-glow group"
            >
              {content?.cta_button_text || "Book Free Demo"}
            </Button>
          </motion.div>
        </section>
      </main>

      <Footer />

      {/* DEMO POPUP MODAL */}
      <Dialog open={demoOpen} onOpenChange={setDemoOpen}>
        <DialogContent className="sm:max-w-sm bg-card border border-border">
          <DialogHeader>
            <DialogTitle className="font-bold text-2xl">Book A Free Demo</DialogTitle>
            <DialogDescription>
              Fill the form and our team will contact you shortly.
            </DialogDescription>
          </DialogHeader>
          <DemoForm />
        </DialogContent>
      </Dialog>
    </>
  );
};

export default AboutUs;