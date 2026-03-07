import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { ArrowRight, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import DemoForm from "@/components/DemoForm";
import { fetchLandingPageContent, LandingPageContent } from "@/services/api";

const FinalCTA = () => {
  const [demoOpen, setDemoOpen] = useState(false);
  const [content, setContent] = useState<LandingPageContent | null>(null);

  useEffect(() => {
    const loadContent = async () => {
      const data = await fetchLandingPageContent();
      if (data) setContent(data);
    };
    loadContent();
  }, []);


  return (
    <>
      <section className="py-20 lg:py-32 bg-hero text-primary-foreground relative overflow-hidden">
        {/* Background decoration */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] rounded-full blur-3xl opacity-10"
            style={{ background: "radial-gradient(ellipse, hsl(43 96% 56%), transparent 70%)" }}
          />
        </div>

        <div className="container relative z-10 text-center max-w-3xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full mb-6
              glass-card border border-yellow-400/30 text-yellow-300 text-sm font-semibold">
              <Sparkles className="w-4 h-4" />
              Join {content?.trusted_retailers_count || "500+"} Happy Retailers
            </div>

            <h2 className="text-3xl lg:text-5xl font-extrabold mb-5 leading-tight tracking-tight">
              Ready to Upgrade{" "}
              <span className="text-gradient-animate">Your Store?</span>
            </h2>
            <p className="text-primary-foreground/65 mb-10 text-lg max-w-xl mx-auto leading-relaxed">
              Join hundreds of Indian retailers who've switched to smarter billing with AI-Setu ERP. Get started in minutes, no tech skills needed.
            </p>

            <Button
              size="lg"
              onClick={() => setDemoOpen(true)}
              className="bg-gold-gradient text-accent-foreground font-bold text-lg px-10 py-6
                shadow-xl transition-all duration-200
                hover:scale-105 hover:shadow-[0_0_40px_rgba(255,200,50,0.5)]
                active:scale-95 animate-pulse-glow group"
            >
              {content?.primary_cta_text || "Book Your Free Demo"}
              <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
            </Button>

            <p className="mt-6 text-sm text-primary-foreground/40">
              No credit card required · Free setup · Cancel anytime
            </p>
          </motion.div>
        </div>
      </section>

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
    </>
  );
};

export default FinalCTA;
