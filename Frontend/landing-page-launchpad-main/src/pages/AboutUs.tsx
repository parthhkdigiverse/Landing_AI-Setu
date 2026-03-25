import Header from "@/components/Header";
import Footer from "@/components/Footer";
import SEO from "@/components/SEO";
import { useRef, useState, useEffect } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { motion, Variants } from "framer-motion";
import { useSearchParams } from "react-router-dom";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";

import DemoForm from "@/components/DemoForm";
import {
  fetchAboutPageContent,
  AboutPageContent,
  Section,
} from "@/services/api";

const AboutUs = () => {
  const [demoOpen, setDemoOpen] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const [content, setContent] = useState<AboutPageContent | null>(null);
  const [livePreview, setLivePreview] = useState<any>(null);

  const [targetSection, setTargetSection] = useState<string | null>(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const isPreview = params.get('is_preview');
    if (isPreview) {
      setTargetSection(params.get('section') || 'all');
    }
  }, []);

  useEffect(() => {
    if (targetSection && targetSection !== 'all') {
      setTimeout(() => {
        const el = document.getElementById(targetSection);
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 800);
    }
  }, [targetSection]);

  useEffect(() => {
    const handler = (event: MessageEvent) => {
      if (event.data?.source === "django-admin") {
        if (event.data.model === 'AboutPageContent' || event.data.model?.toLowerCase().includes('about')) {
          const payload = event.data.payload;
          let parsedPayload = { ...payload };

          const serve_items: any[] = [];
          const why_choose_items: any[] = [];

          Object.keys(payload).forEach(key => {
            if (key.includes('TOTAL_FORMS') || key.includes('INITIAL_FORMS') || key.includes('MAX_NUM_FORMS') || key.includes('MIN_NUM_FORMS')) return;

            if (key.startsWith('aboutusserveitem_set-')) {
                const parts = key.split('-');
                if (parts.length >= 3) {
                    const idx = parseInt(parts[1], 10);
                    const field = parts.slice(2).join('-');
                    if (!serve_items[idx]) serve_items[idx] = {};
                    serve_items[idx][field] = payload[key];
                }
            } else if (key.startsWith('aboutuswhychooseitem_set-')) {
                const parts = key.split('-');
                if (parts.length >= 3) {
                    const idx = parseInt(parts[1], 10);
                    const field = parts.slice(2).join('-');
                    if (!why_choose_items[idx]) why_choose_items[idx] = {};
                    why_choose_items[idx][field] = payload[key];
                }
            }
          });

          if (serve_items.length > 0) parsedPayload.serve_items = serve_items.filter(Boolean);
          if (why_choose_items.length > 0) parsedPayload.why_choose_items = why_choose_items.filter(Boolean);

          setLivePreview((prev: any) => ({ ...prev, ...parsedPayload }));
        }

        if (event.data.scrollTarget) {
          const el = document.getElementById(event.data.scrollTarget);
          if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
        }
      }
    };
    window.addEventListener("message", handler);
    return () => window.removeEventListener("message", handler);
  }, []);

  useEffect(() => {
    const loadData = async () => {
      const data = await fetchAboutPageContent();
      if (data) setContent(data);
    };
    loadData();
  }, []);

  // ✅ IMAGE FIX (GLOBAL)
  const getImageUrl = (path?: string) => {
    if (!path) return "/placeholder.png";
    return path.startsWith("http")
      ? path
      : path; // Relative path works on any origin
  };

  // ANIMATIONS
  const fadeUp: Variants = {
    hidden: { opacity: 0, y: 60, scale: 0.97 },
    show: {
      opacity: 1,
      y: 0,
      scale: 1,
      transition: { duration: 0.7 },
    },
  };

  const fadeIn: Variants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { duration: 0.8 },
    },
  };

  const stagger: Variants = {
    hidden: {},
    show: {
      transition: { staggerChildren: 0.15 },
    },
  };

  const getSection = (name: string): Section | undefined =>
    content?.sections?.find((s) => s.name === name);

  const scroll = (direction: "left" | "right") => {
    if (!scrollRef.current) return;
    scrollRef.current.scrollBy({
      left: direction === "left" ? -320 : 320,
      behavior: "smooth",
    });
  };

  const hero = getSection("hero");
  const about = getSection("about");
  const mission = getSection("mission");
  const why = getSection("why_choose");
  const serve = getSection("serve");
  const cta = getSection("cta");

  // Helper to conditionally render active section
  const shouldShowSection = (id: string) => {
    if (!targetSection || targetSection === 'all') return true;
    return targetSection === id;
  };

  return (
    <>
      <SEO 
        title={content?.seo_title || "About Us"} 
        description={content?.seo_description || "Learn more about AI Setu's mission to empower retailers with innovative AI solutions. Meet our team and discover our journey."}
        keywords={content?.seo_keywords || "about AI Setu, company mission, retail innovation team"}
      />
      {!targetSection && <Header />}

      <main className="bg-[#F5F6FA]">

        {/* HERO */}
        {shouldShowSection('hero') && (
        <motion.section
          id="hero"
          variants={fadeIn}
          initial="hidden"
          animate="show"
          className="bg-[#1F2E4D] text-white py-20 text-center"
        >
          <motion.div variants={fadeUp} className="text-[#F4B400] font-bold tracking-wider uppercase mb-4 text-sm">
            {livePreview?.about_label || (content as any)?.about_label || "ABOUT US"}
          </motion.div>
          <motion.h1 variants={fadeUp} className="text-5xl font-bold mb-4">
            {livePreview?.hero_title || hero?.title || "About AI-Setu ERP"}
          </motion.h1>

          <motion.p variants={fadeUp} className="max-w-3xl mx-auto text-gray-300">
            {livePreview?.hero_description || hero?.subtitle || "AI-Setu ERP empowers retailers with modern technology to simplify store management. We help SMEs automate operations, improve efficiency, and grow faster with intelligent ERP solutions."}
          </motion.p>
        </motion.section>
        )}

        {/* ABOUT */}
        {shouldShowSection('story') && (
        <motion.section
          id="about"
          variants={fadeIn}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true }}
          className="py-20 bg-white"
        >
          <motion.div
            variants={stagger}
            className="max-w-7xl mx-auto grid md:grid-cols-2 gap-12 px-6"
          >
            <motion.div variants={fadeUp}>
              <h3 className="text-[#F4B400] font-bold tracking-wider uppercase mb-2 text-sm">
                ABOUT US
              </h3>
              <h2 className="text-3xl font-bold mb-4">{livePreview?.about_heading || about?.title}</h2>
              <p className="mb-4 text-gray-600">{about?.subtitle}</p>

              {livePreview ? (
                <>
                  {livePreview.about_description_1 && <p className="text-gray-600 mb-2">{livePreview.about_description_1}</p>}
                  {livePreview.about_description_2 && <p className="text-gray-600 mb-2">{livePreview.about_description_2}</p>}
                  {livePreview.about_description_3 && <p className="text-gray-600 mb-2">{livePreview.about_description_3}</p>}
                </>
              ) : (
                about?.items?.map((item) => (
                  <p key={item.id} className="text-gray-600 mb-2">
                    {item.description}
                  </p>
                ))
              )}
            </motion.div>

            {about?.image && (
              <img
                src={about.image}  
                className="rounded-lg shadow"
              />
            )}
          </motion.div>
        </motion.section>
        )}

        {/* MISSION + WHY */}
        {(shouldShowSection('mission') || shouldShowSection('why')) && (
        <motion.section
          id="mission"
          variants={fadeIn}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true }}
          className="py-20"
        >
          <motion.div
            variants={stagger}
            className={`mx-auto grid ${(shouldShowSection('mission') && shouldShowSection('why')) ? 'max-w-6xl md:grid-cols-2 gap-12' : 'max-w-3xl md:grid-cols-1 gap-6'} px-6`}
          >
            {shouldShowSection('mission') && (
            <motion.div variants={fadeUp} className={(shouldShowSection('mission') && !shouldShowSection('why')) ? 'text-center' : ''}>
              <h2 className="text-3xl font-bold mb-4">{livePreview?.mission_title || mission?.title}</h2>
              <p className="text-gray-600">{livePreview?.mission_description || mission?.subtitle}</p>
            </motion.div>
            )}

            {shouldShowSection('why') && (
            <motion.div variants={fadeUp} className="bg-white p-6 rounded-lg shadow" id="why_choose">
              <h3 className="text-xl font-semibold mb-3">{livePreview?.why_choose_title || why?.title}</h3>
              <ul className="space-y-2 text-gray-600">
                {livePreview ? (
                  <>
                    {/* Dynamic points only */}
                    {livePreview.why_choose_items?.map((item: any, idx: number) => (
                      !item.DELETE && item.title && <li key={`dynamic-${idx}`}>✔ {item.title}</li>
                    ))}
                  </>
                ) : (
                  why?.items?.map((item) => (
                    <li key={item.id}>✔ {item.title}</li>
                  ))
                )}
              </ul>
            </motion.div>
            )}
          </motion.div>
        </motion.section>
        )}

        {/* SERVE */}
        {shouldShowSection('serve') && (
        <motion.section
          id="serve"
          variants={fadeIn}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true }}
          className="py-20"
        >
          <h2 className="text-center text-3xl font-bold mb-4">{livePreview?.serve_title || serve?.title}</h2>
          <p className="text-center mb-8 text-black-300">{livePreview?.serve_subtitle || serve?.subtitle}</p>

          <div className="relative max-w-7xl mx-auto px-6">

            <button
              onClick={() => scroll("left")}
              className="absolute left-6 top-1/2 -translate-y-1/2 z-10 
              bg-white text-black hover:bg-[#F4B400] hover:text-white
              p-3 rounded-full shadow-md border border-gray-200
              transition-all duration-300 hover:scale-110 active:scale-90"
            >
              <ChevronLeft size={20} />
            </button>

            <button
              onClick={() => scroll("right")}
              className="absolute right-6 top-1/2 -translate-y-1/2 z-10 
              bg-white text-black hover:bg-[#F4B400] hover:text-white
              p-3 rounded-full shadow-md border border-gray-200
              transition-all duration-300 hover:scale-110 active:scale-90"
            >
              <ChevronRight size={20} />
            </button>

            <div
              ref={scrollRef}
              className="flex gap-8 overflow-x-auto px-6 no-scrollbar scroll-smooth"
            >
              {(livePreview?.serve_items || serve?.items)?.map((item: any, idx: number) => {
                const originalItem = serve?.items?.find(x => x.id == item.id) || serve?.items?.[idx];
                const finalImage = item.image || originalItem?.image;

                return (
                <div
                  key={item.id || idx}
                  className="min-w-[300px] h-[200px] relative rounded-xl overflow-hidden shadow-lg group"
                >
                  {finalImage && (
                    <img
                      src={finalImage}
                      className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                    />
                  )}

                  <div className="absolute inset-0 bg-black/30"></div>

                  <div className="absolute bottom-4 left-4 text-white font-semibold text-base">
                    {item.title}
                  </div>
                </div>
                );
              })}
            </div>

          </div>
        </motion.section>
        )}

        {/* CTA */}
        {shouldShowSection('cta') && (
        <motion.section
          id="cta"
          variants={fadeUp}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true }}
          className="py-20 bg-[#1F2E4D] text-white text-center"
        >
          <h2 className="text-3xl font-bold mb-3">{livePreview?.cta_title || cta?.title}</h2>
          <p className="mb-4 text-gray-300">{livePreview?.cta_description || cta?.subtitle}</p>

          <motion.div whileHover={{ scale: 1.1 }}>
            <Button
              size="lg"
              className="bg-gold-gradient text-accent-foreground font-bold text-lg px-10 py-6 shadow-xl"
              onClick={() => setDemoOpen(true)}
            >
              {livePreview?.cta_button_text || cta?.items?.[0]?.title || "Book Demo"}
            </Button>
          </motion.div>
        </motion.section>
        )}

      </main>

      {!targetSection && <Footer />}

      <Dialog open={demoOpen} onOpenChange={setDemoOpen}>
        <DialogContent className="sm:max-w-sm bg-card border border-border">
          <DialogHeader>
            <DialogTitle className="text-2xl font-bold">
              Book A Free Demo
            </DialogTitle>
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