import { motion } from "framer-motion";
import { Gift, RefreshCw, Infinity, UserPlus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState, useEffect } from "react";
import axios from "axios";
import { toast, Toaster } from "react-hot-toast";
import { fetchLandingPageContent, fetchReferralPerks } from "@/services/api";

const iconMap: any = {
  gift: Gift,
  renewal: RefreshCw,
  user: UserPlus,
  unlimited: Infinity
};

const ReferralSection = () => {
  const [content, setContent] = useState<any>(null);
  const [livePreview, setLivePreview] = useState<any>(null);
  const [perks, setPerks] = useState<any[]>([]);
  const [mobile, setMobile] = useState("");
  const [referralCode, setReferralCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  // Fetch DB content (for text + button)
  useEffect(() => {
    const loadContent = async () => {
      const data = await fetchLandingPageContent();
      if (data) setContent(data);
    };
    loadContent();
  }, []);

  // Fetch perks (CRUD)
  useEffect(() => {
    const loadPerks = async () => {
      try{
        const res = await fetch("/api/referral-perks/");
        const data = await res.json();
        setPerks(data);
      }catch(err){
        console.error("Referral perks error", err);
      }
    };
    loadPerks();
  }, []);

  // Live preview listener
  useEffect(() => {
    const handler = (event: any) => {
      if (event.data && event.data.source === 'django-admin') {
        if (event.data.model === 'LandingPageContent' || event.data.model === 'ReferralProgramContent') {
          setContent((prev: any) => ({ ...prev, ...event.data.payload }));
        } else if (event.data.model === 'ReferralPerk') {
          const item = event.data.payload;
          const pk = event.data.pk;
          setPerks(prev => prev.map(p => (p.id === parseInt(pk) || p.id === pk) ? { ...p, ...item } : p));
        }
      }
    };
    window.addEventListener("message", handler);
    return () => window.removeEventListener("message", handler);
  }, []);

  // Robust copy function with fallback for non-HTTPS/non-secure contexts
  const copyToClipboard = async (text: string) => {
    if (navigator.clipboard && window.isSecureContext) {
      try {
        await navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
        return true;
      } catch (err) {
        console.error("Clipboard API failed", err);
      }
    }

    // Fallback: Use a temporary hidden textarea
    try {
      const textArea = document.createElement("textarea");
      textArea.value = text;
      textArea.style.position = "fixed";
      textArea.style.left = "-9999px";
      textArea.style.top = "0";
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      const successful = document.execCommand("copy");
      document.body.removeChild(textArea);
      if (successful) {
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      }
      return successful;
    } catch (err) {
      console.error("Fallback copy failed", err);
      return false;
    }
  };

  // Handle mobile number submit
  const submitMobile = async () => {
    if (!mobile) return toast.error("Please enter mobile number");
    setLoading(true);

    try {
      const res = await axios.post("/referral-check/", {
        mobile_number: mobile
      });
      const newCode = res.data.referral_code;
      setReferralCode(newCode);

      // --- NEW LOGIC: Auto-copy to clipboard ---
      const wasCopied = await copyToClipboard(newCode);

      // --- Updated Toast Message ---
      if (wasCopied) {
        toast.success("Referral code generated and copied to clipboard!");
      } else {
        toast.success("Referral code generated! (Copy manually if needed)");
      }
      
    } catch (error: any) {
      if (error.response?.data?.error) {
        toast.error(error.response.data.error);
      } else {
        toast.error("Something went wrong");
      }
      console.error(error);
    }

    setLoading(false);
  };

  const handleManualCopy = () => {
    copyToClipboard(referralCode);
    toast.success("Referral code copied!");
  };

  return (
    <section className="py-16 lg:py-24 bg-hero text-primary-foreground">
      <Toaster position="top-right" reverseOrder={false} />
      <div className="container">

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <span className="text-accent font-semibold text-sm uppercase tracking-wider">
            {livePreview?.referral_label || content?.referral_label || "Referral Program"}
          </span>

          <h2 className="text-3xl lg:text-4xl font-bold mt-2">
            {livePreview?.referral_title || content?.referral_title || "Earn With AI-Setu ERP"}
          </h2>
        </motion.div>

        {/* Perks */}
        <div className="grid md:grid-cols-4 gap-8 max-w-4xl mx-auto mb-10">
          {(content?.referral_perks || perks).map((p: any, i: number) => {
            const Icon = iconMap[p.icon];
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="text-center"
              >
                <div className="w-14 h-14 rounded-xl bg-accent/20 flex items-center justify-center mx-auto mb-3">
                  {Icon && <Icon className="h-7 w-7 text-accent" />}
                </div>
                <h3 className="text-2xl font-bold text-gradient-gold">{p.value}</h3>
                <p className="text-primary-foreground/70 text-sm mt-1">{p.text}</p>
              </motion.div>
            );
          })}
        </div>

        {/* Mobile Input + Button + Referral Code */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            submitMobile();
          }}
          className="flex flex-col sm:flex-row items-center justify-center gap-4"
        >
          <input
            type="tel"
            placeholder="Enter Mobile Number"
            value={mobile}
            onChange={(e) => setMobile(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                e.stopPropagation();
                submitMobile();
              }
            }}
            className="border border-gray-300 dark:border-gray-600 rounded-lg px-4 py-3
                       placeholder:text-gray-400 dark:placeholder:text-gray-400
                       text-black dark:text-black
                       focus:ring-2 focus:ring-gold-gradient focus:outline-none dark:bg-gray-100"
          />
          <Button
            type="submit"
            disabled={loading}
            className="bg-gold-gradient text-accent-foreground font-semibold hover:opacity-90 px-6 py-3"
          >
            {loading ? "Checking..." : (livePreview?.join_referral || content?.join_referral || "Join Referral Program")}
          </Button>

          {referralCode && (
            <div className="flex items-center gap-2 ml-4 bg-yellow-100 text-yellow-700 px-4 py-3 rounded-lg">
              <span className="font-bold">{referralCode}</span>
              <button
                type="button"
                onClick={handleManualCopy}
                className="text-yellow-800 hover:text-yellow-900"
              >
                Copy
              </button>
            </div>
          )}
        </form>
      </div>
    </section>
  );
};

export default ReferralSection;