import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Play, Sparkles, ArrowRight, CheckCircle2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import DemoForm from "@/components/DemoForm";
import heroImg from "@/assets/image.png";
import aiScanImg from "@/assets/ai-scan.jpg";
import { fetchLandingPageContent, LandingPageContent } from "@/services/api";
import { fetchDemoVideo } from "@/services/api";

const defaultHighlights = [
  "GST-Ready Billing",
  "Real-time Inventory",
  "AI-Powered Insights",
];

interface HeroSectionProps {
  content?: LandingPageContent | null;
}

const HeroSection = ({ content: propContent }: HeroSectionProps) => {
  const [demoOpen, setDemoOpen] = useState(false);
  const [videoOpen, setVideoOpen] = useState(false);
  const [content, setContent] = useState<LandingPageContent | null>(propContent || null);
  const [demoVideoUrl, setDemoVideoUrl] = useState<string | null>(null);
  

  // Sync state if prop changes
  useEffect(() => {
    if (propContent) {
      setContent(propContent);
    }
  }, [propContent]);

  useEffect(() => {
  const loadVideo = async () => {
    const video = await fetchDemoVideo();

    if (video?.video_url) {
      setDemoVideoUrl(video.video_url);
    }
  };

  loadVideo();
}, []);

  useEffect(() => {
    if (propContent) return;

    const loadContent = async () => {
      const data = await fetchLandingPageContent();
      if (data) {
        setContent(data);
      }
    };
    loadContent();
  }, [propContent]);

  useEffect(() => {

    const handler = (event: MessageEvent) => {
      if (event.data && typeof event.data === 'object' && !Array.isArray(event.data) && event.data.source === 'django-admin') {
        setContent((prev: any) => ({
          ...prev,
          ...event.data.payload
        }));
      }
    };

  window.addEventListener("message", handler)

  return () => window.removeEventListener("message", handler)

},[])

  const highlights = content?.hero_highlights
    ? content.hero_highlights.split(",").map((h) => h.trim())
    : defaultHighlights;

  const isPreview = typeof window !== 'undefined' ? new URLSearchParams(window.location.search).get('is_preview') === '1' : false;

  return (
    <>
      <section className={`bg-hero text-primary-foreground relative flex items-center ${isPreview ? 'min-h-[500px]' : 'min-h-screen lg:min-h-[90vh] py-20 lg:py-0'}`}>

        {/* Background blobs container - isolates overflow-hidden to prevent horizontal scroll while allowing section to grow vertically */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div
            className="absolute top-0 left-0 w-[600px] h-[600px] rounded-full opacity-10 blur-3xl"
            style={{
              background:
                "radial-gradient(circle, hsl(43 96% 56% / 0.6), transparent 70%)",
              transform: "translate(-30%, -40%)",
            }}
          />

          <div
            className="absolute bottom-0 right-0 w-[500px] h-[500px] rounded-full opacity-10 blur-3xl"
            style={{
              background:
                "radial-gradient(circle, hsl(220 80% 60% / 0.5), transparent 70%)",
              transform: "translate(20%, 30%)",
            }}
          />
        </div>

        <div className={`container relative z-10 grid lg:grid-cols-2 gap-10 lg:gap-16 items-center ${isPreview ? 'py-8' : 'py-12 md:py-16 lg:py-24'}`}>

          {/* LEFT COLUMN */}
          <motion.div
            initial={isPreview ? { opacity: 1, y: 0 } : { opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, ease: "easeOut" }}
            className="text-center lg:text-left flex flex-col items-center lg:items-start order-1 lg:order-none"
          >
            {/* Eyebrow */}
            <motion.div
              initial={{ opacity: 0, scale: 0.85 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.15, duration: 0.4 }}
              className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full mb-6
                glass-card border border-yellow-400/30 text-yellow-300 text-sm font-semibold"
            >
              <Sparkles className="w-4 h-4 animate-pulse" />

              {
                content?.hero_eyebrow ||
                "India's Smartest Retail ERP"} 
            </motion.div>

            <h1 className="text-3xl sm:text-4xl lg:text-5xl xl:text-[3.8rem] font-extrabold leading-[1.1] mb-6 tracking-tight">
              { content?.hero_title || "Smart ERP for"}{" "}
              <span className="text-gradient-animate">
                {
                  content?.hero_highlighted_title ||
                  "Indian Retailers"}
              </span>
            </h1>

            <p className="text-base sm:text-lg lg:text-xl text-primary-foreground/75 mb-8 max-w-lg leading-relaxed whitespace-pre-line mx-auto lg:mx-0">
              {
                content?.hero_subtitle ||
                "AI-powered billing, inventory & store management — built specifically for Indian retail businesses."}
            </p>

            {/* Highlight pills */}
            <div className="flex flex-wrap justify-center lg:justify-start gap-3 mb-10">
              {highlights.map((h: string) => (
                <span
                  key={h}
                  className="inline-flex items-center gap-1.5 text-xs sm:text-sm px-3 py-1 rounded-full
                  bg-white/10 text-primary-foreground/90 border border-white/15 font-medium"
                >
                  <CheckCircle2 className="w-3.5 h-3.5 text-yellow-400" />
                  {h}
                </span>
              ))}
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-wrap justify-center lg:justify-start gap-4">

              <Button
                size="lg"
                onClick={() => setDemoOpen(true)}
                className="bg-gold-gradient text-accent-foreground font-bold text-sm sm:text-base px-6 sm:px-8 py-5 sm:py-6
                  transition-all duration-200 shadow-lg
                  hover:scale-105 hover:shadow-[0_0_28px_rgba(255,200,50,0.55)]
                  active:scale-95 animate-pulse-glow group"
              >
                {
                  content?.primary_cta_text ||
                  "Book Free Demo"}

                <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </Button>

              {demoVideoUrl && (
                <Button
                  size="lg"
                  variant="outline"
                  className="border-white/25 text-primary-foreground bg-white/5 backdrop-blur-sm
                    hover:bg-white/15 hover:border-white/40 transition-all duration-200 px-6 sm:px-8 py-5 sm:py-6 font-semibold text-sm sm:text-base"
                  onClick={() => setVideoOpen(true)}
                >
                  <Play className="mr-2 h-4 w-4 fill-current" />

                  {
                    content?.secondary_cta_text ||
                    "Watch Demo"}
                </Button>
              )}
            </div>

            {/* Social Proof */}
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6 }}
              className="mt-8 text-xs sm:text-sm text-primary-foreground/50"
            >
              ⭐⭐⭐⭐⭐ Trusted by{" "}
              <span className="text-yellow-400 font-semibold">
                {
                  content?.trusted_retailers_count ||
                  "500+"}
              </span>{" "}
              Indian retailers
            </motion.p>
          </motion.div>

          {/* RIGHT COLUMN */}
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
            className="relative flex items-center justify-center pb-8 lg:pb-12 lg:pr-4 order-2 lg:order-none scale-90 sm:scale-100"
          >
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
              <div
                className="w-[300px] h-[300px] sm:w-[420px] sm:h-[420px] rounded-full opacity-25 blur-2xl"
                style={{
                  background:
                    "radial-gradient(circle, hsl(43 96% 56%), transparent 70%)",
                }}
              />
            </div>

            <div className="relative w-full max-w-[480px] animate-float">
              <div
                className="absolute -inset-[3px] rounded-3xl opacity-60 blur-sm pointer-events-none"
                style={{
                  background:
                    "linear-gradient(135deg, hsl(43 96% 56% / 0.6), transparent 60%)",
                }}
              />

              <img
                src={heroImg}
                alt="AI-Setu ERP Dashboard"
                className="relative rounded-2xl shadow-2xl w-full object-cover border border-white/15"
              />

              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.8, duration: 0.5 }}
                className="absolute -top-3 -right-3 sm:-top-5 sm:-right-5 glass-card rounded-xl px-3 sm:px-4 py-2 sm:py-2.5 shadow-xl border border-yellow-400/20"
              >
                <p className="text-[10px] sm:text-xs text-primary-foreground/60 font-medium">
                  {
                    content?.hero_stats_label ||
                    "Today's Sales"}
                </p>

                <p className="text-lg sm:text-xl font-bold text-yellow-400">
                  {
                    content?.hero_stats_value ||
                    "₹1,24,500"}
                </p>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 1 }}
                className="absolute -bottom-2 -right-2 sm:-bottom-4 sm:-right-4 glass-card rounded-xl px-2.5 sm:px-3 py-1.5 sm:py-2 shadow-xl
                  border border-white/15 flex items-center gap-2"
              >
                <span className="w-1.5 h-1.5 sm:w-2 sm:h-2 rounded-full bg-green-400 animate-pulse" />
                <span className="text-[10px] sm:text-xs font-semibold text-primary-foreground/80">
                  AI Active
                </span>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: 0.9 }}
                className="absolute -bottom-6 -left-6 sm:-bottom-8 sm:-left-8 w-28 sm:w-40 rounded-xl overflow-hidden shadow-2xl
                  border-2 border-white/15 ring-2 ring-yellow-400/20"
              >
                <img
                  src={aiScanImg}
                  alt="AI Scan Feature"
                  className="w-full object-cover"
                />
              </motion.div>
            </div>
          </motion.div>
        </div>

        <div className="absolute bottom-0 left-0 right-0 h-16 bg-gradient-to-t from-background/20 to-transparent pointer-events-none" />
      </section>

      {/* DEMO FORM MODAL */}
      <Dialog open={demoOpen} onOpenChange={setDemoOpen}>
        <DialogContent className="sm:max-w-sm bg-card border border-border">
          <DialogHeader>
            <DialogTitle className="font-heading font-bold text-2xl text-foreground">
              Book A Free Demo
            </DialogTitle>

            <DialogDescription className="text-sm text-muted-foreground">
              Fill the form and our team will contact you shortly.
            </DialogDescription>
          </DialogHeader>

          <DemoForm />
        </DialogContent>
      </Dialog>

      {/* VIDEO MODAL */}
      {videoOpen && (
        <div
          className="fixed inset-0 bg-black/70 flex items-center justify-center z-50"
          onClick={() => setVideoOpen(false)}
        >
          <div
            className="bg-white p-4 rounded-lg w-[800px] max-w-full relative"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              className="absolute top-2 right-3 text-black text-xl"
              onClick={() => setVideoOpen(false)}
            >
              ✕
            </button>

            <iframe
              width="100%"
              height="450"
              src={demoVideoUrl}
              title="Demo Video"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              referrerPolicy="strict-origin-when-cross-origin"
              allowFullScreen
              className="rounded"
            />
          </div>
        </div>
      )}
    </>
  );
};

export default HeroSection;