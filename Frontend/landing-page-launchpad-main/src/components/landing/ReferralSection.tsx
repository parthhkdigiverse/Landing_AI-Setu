import { motion } from "framer-motion";
import { Gift, RefreshCw, Infinity, UserPlus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState, useEffect } from "react";
import axios from "axios";
import { toast, Toaster } from "react-hot-toast";
import { fetchLandingPageContent } from "@/services/api";

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
      try {
        const res = await fetch("http://127.0.0.1:8000/api/referral-perks/");
        const data = await res.json();
        setPerks(data);
      } catch (err) {
        console.error("Referral perks error", err);
      }
    };
    loadPerks();
  }, []);

  // Live preview listener
  useEffect(() => {
    const handler = (event: any) => {
      if (event.data) {
        setLivePreview((prev: any) => ({ ...prev, ...event.data }));
      }
    };
    window.addEventListener("message", handler);
    return () => window.removeEventListener("message", handler);
  }, []);

  // Handle mobile number submit
  const submitMobile = async () => {
    if (!mobile) return toast.error("Please enter mobile number");
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/referral-check/", {
        mobile_number: mobile
      });
      setReferralCode(res.data.referral_code);
      toast.success("Referral code generated!");
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

  const copyToClipboard = () => {
    navigator.clipboard.writeText(referralCode);
    setCopied(true);
    toast.success("Referral code copied!");
    setTimeout(() => setCopied(false), 2000);
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
          {perks.map((p, i) => {
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
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <input
            type="text"
            placeholder="Enter Mobile Number"
            value={mobile}
            onChange={(e) => setMobile(e.target.value)}
            className="border border-gray-300 dark:border-gray-600 rounded-lg px-4 py-3
                       placeholder:text-gray-400 dark:placeholder:text-gray-400
                       text-black dark:text-black
                       focus:ring-2 focus:ring-gold-gradient focus:outline-none dark:bg-gray-100"
          />
          <Button
            onClick={submitMobile}
            disabled={loading}
            className="bg-gold-gradient text-accent-foreground font-semibold hover:opacity-90 px-6 py-3"
          >
            {loading ? "Checking..." : (livePreview?.join_referral || content?.join_referral || "Join Referral Program")}
          </Button>

          {referralCode && (
            <div className="flex items-center gap-2 ml-4 bg-yellow-100 text-yellow-700 px-4 py-3 rounded-lg">
              <span className="font-bold">{referralCode}</span>
              <button
                onClick={copyToClipboard}
                className="text-yellow-800 hover:text-yellow-900"
              >
                Copy
              </button>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};

export default ReferralSection;