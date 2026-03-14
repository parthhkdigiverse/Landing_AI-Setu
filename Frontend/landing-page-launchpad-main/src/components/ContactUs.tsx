import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "sonner";
import { motion } from "framer-motion";
import { Mail, Phone, MapPin, Clock, Send, MessageSquare, Users, Zap } from "lucide-react";
// Import the specific function and API_BASE_URL from your api.ts
import { fetchContactPageContent, ContactPageContent, API_BASE_URL } from "@/services/api";

// Assuming submitContactForm is also in your api.ts, if not, define it here
export const submitContactForm = async (data: any) => {
  const response = await fetch(`${API_BASE_URL}/api/contact/submit/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return response.json();
};

const ContactUsPage = () => {
  // 1. STATE MANAGEMENT
  const [content, setContent] = useState<ContactPageContent | null>(null);
  const [formData, setFormData] = useState({
    name: "",
    phone: "",
    email: "",
    officeAddress: "",
    message: "",
  });

  // 2. FETCH DATA ON MOUNT
  useEffect(() => {
    const loadData = async () => {
      const data = await fetchContactPageContent();
      if (data) {
        setContent(data);
      }
    };
    loadData();
  }, []);

  // 3. LIVE PREVIEW LISTENER (For Django Admin)
  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      if (event.data && typeof event.data === "object") {
        setContent((prev) => ({
          ...prev,
          ...event.data,
        } as ContactPageContent));
      }
      if (event.data === "reload_full_data") {
        fetchContactPageContent().then((data) => data && setContent(data));
      }
    };

    window.addEventListener("message", handleMessage);
    return () => window.removeEventListener("message", handleMessage);
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await submitContactForm(formData);
      if (res.message) {
        toast.success(res.message);
        setFormData({ name: "", phone: "", email: "", officeAddress: "", message: "" });
      }
    } catch (err) {
      toast.error("Server error. Please try again later.");
    }
  };

  // 4. GUARD: Prevent crash if content is not yet loaded
  if (!content) {
    return (
      <div className="h-screen flex items-center justify-center bg-[#1F2E4D] text-white">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#F4B400]"></div>
      </div>
    );
  }

  // Helper for dynamic cards
  const contactInfo = [
    { icon: Phone, title: content.call_title, details: content.call_phone, sub: content.call_subtext, color: "from-blue-500 to-cyan-500" },
    { icon: Mail, title: content.email_title, details: content.email_address, sub: content.email_subtext, color: "from-purple-500 to-pink-500" },
    { icon: MapPin, title: content.visit_title, details: content.visit_address, sub: content.visit_subtext, color: "from-green-500 to-emerald-500" },
    { icon: Clock, title: content.support_title, details: content.support_time, sub: content.support_subtext, color: "from-orange-500 to-red-500" }
  ];

  return (
    <>
      <Header />

      {/* HERO SECTION */}
      <section className="relative min-h-[60vh] bg-gradient-to-br from-[#1F2E4D] via-[#2D3748] to-[#1A202C] flex items-center">
        <div className="relative z-10 container mx-auto px-6 py-20 text-center">
          <motion.h1 initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-6xl font-bold text-white mb-6">
            {content.hero_title}
          </motion.h1>
          <motion.p initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="text-xl text-gray-300 max-w-2xl mx-auto">
            {content.hero_description}
          </motion.p>
        </div>
      </section>

      {/* CONTACT INFO CARDS */}
      <section className="py-16 bg-[#F5F6FA]">
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 -mt-24 relative z-20">
            {contactInfo.map((info, idx) => (
              <motion.div key={idx} whileHover={{ y: -5 }} className="bg-white rounded-2xl p-6 shadow-xl border border-gray-100">
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${info.color} flex items-center justify-center mb-4`}>
                  <info.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-lg font-bold text-[#1F2E4D] mb-2">{info.title}</h3>
                <p className="text-[#1F2E4D] font-semibold mb-1">{info.details}</p>
                <p className="text-gray-600 text-sm">{info.sub}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* MAIN CONTENT SECTION */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-6 grid lg:grid-cols-2 gap-16 max-w-7xl">
          
          {/* FORM SIDE */}
          <div>
            <h2 className="text-4xl font-bold text-[#1F2E4D] mb-8">{content.form_title}</h2>
            <form onSubmit={handleSubmit} className="bg-white shadow-2xl rounded-3xl p-8 border border-gray-100 space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-[#1F2E4D]">{content.name_label}</label>
                  <Input name="name" placeholder={content.name_placeholder} value={formData.name} onChange={handleChange} required />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-[#1F2E4D]">{content.phone_label}</label>
                  <Input name="phone" placeholder={content.phone_placeholder} value={formData.phone} onChange={handleChange} required />
                </div>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-semibold text-[#1F2E4D]">{content.email_label}</label>
                <Input name="email" type="email" placeholder={content.email_placeholder} value={formData.email} onChange={handleChange} required />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-semibold text-[#1F2E4D]">{content.company_label}</label>
                <Input name="officeAddress" placeholder={content.company_placeholder} value={formData.officeAddress} onChange={handleChange} required />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-semibold text-[#1F2E4D]">{content.message_label}</label>
                <Textarea name="message" placeholder={content.message_placeholder} value={formData.message} onChange={handleChange} required className="min-h-[120px] resize-none" />
              </div>
              <Button type="submit" className="w-full h-14 bg-[#F4B400] text-white font-bold text-lg rounded-xl shadow-lg hover:bg-[#E6A800] transition-all">
                <Send className="w-5 h-5 mr-2" />
                {content.form_button_text}
              </Button>
            </form>
          </div>

          {/* FEATURES SIDE */}
          <div className="space-y-12">
            <div>
              <h2 className="text-4xl font-bold text-[#1F2E4D] mb-6">{content.why_title}</h2>
              <p className="text-lg text-gray-600 leading-relaxed">{content.why_description}</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {[
                { icon: Users, text: content.feature_1_title, color: "text-blue-600" },
                { icon: Zap, text: content.feature_2_title, color: "text-purple-600" },
                { icon: MessageSquare, text: content.feature_3_title, color: "text-green-600" },
                { icon: Send, text: content.feature_4_title, color: "text-orange-600" }
              ].map((feat, i) => (
                <div key={i} className="bg-white rounded-2xl p-6 border shadow-sm flex items-center gap-4">
                  <feat.icon className={`w-8 h-8 ${feat.color}`} />
                  <span className="font-semibold text-[#1F2E4D]">{feat.text}</span>
                </div>
              ))}
            </div>

            {/* CTA BLOCK */}
            <div className="bg-[#F4B400]/10 rounded-2xl p-8 border border-[#F4B400]/20">
              <h3 className="text-2xl font-bold text-[#1F2E4D] mb-4">{content.cta_title}</h3>
              <p className="text-gray-600 mb-6">{content.cta_description}</p>
              <div className="flex flex-wrap gap-4 text-xs font-bold uppercase tracking-wider text-gray-500">
                <span>• {content.cta_button_text1}</span>
                <span>• {content.cta_button_text2}</span>
                <span>• {content.cta_button_text3}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
};

export default ContactUsPage;