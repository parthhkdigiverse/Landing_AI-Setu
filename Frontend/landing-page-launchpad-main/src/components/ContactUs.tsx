import Header from "@/components/Header";
import Footer from "@/components/Footer";
import SEO from "@/components/SEO";
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
      if (event.data && typeof event.data === "object" && event.data.source === "django-admin") {
        setContent((prev) => ({
          ...prev,
          ...event.data.payload,
        } as ContactPageContent));
        
        if (event.data.scrollTarget) {
            setTimeout(() => {
                const el = document.getElementById(event.data.scrollTarget);
                if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 100);
        }
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

  const sectionParam = typeof window !== 'undefined' ? new URLSearchParams(window.location.search).get('section') : null;
  const isPreview = typeof window !== 'undefined' ? new URLSearchParams(window.location.search).get('is_preview') === '1' : false;

  // Helper to determine if a section should be shown
  const shouldShow = (id: string, toggle?: boolean) => {
    if (isPreview && sectionParam === id) return true;
    if (toggle === false) return false;
    if (isPreview && sectionParam && sectionParam !== id) return false;
    return true;
  };

  // Helper for dynamic cards
  const contactInfo = [
    { 
      icon: Phone, 
      title: content.call_title, 
      details: content.call_phone, 
      sub: content.call_subtext, 
      color: "from-blue-500 to-cyan-500",
      action: () => window.location.href = `tel:${content.call_phone_number.replace(/\s+/g, '')}`
    },
    { 
      icon: Mail, 
      title: content.email_title, 
      details: content.email_address, 
      sub: content.email_subtext, 
      color: "from-purple-500 to-pink-500",
      action: () => window.location.href = `mailto:${content.email_address_link}`
    },
    { 
      icon: MapPin, 
      title: content.visit_title, 
      details: content.visit_address, 
      sub: content.visit_subtext, 
      color: "from-green-500 to-emerald-500",
      action: () => window.open(content.visit_map_url, '_blank')
    },
    { 
      icon: Clock, 
      title: content.support_title, 
      details: content.support_time, 
      sub: content.support_subtext, 
      color: "from-orange-500 to-red-500",
      action: null 
    }
  ];

  return (
    <>
      <SEO 
        title={content.seo_title || content.hero_title || "Contact Us"} 
        description={content.seo_description || content.hero_description || "Get in touch with AI Setu for any queries, support, or demo requests. We are here to help your business grow."}
        keywords={content.seo_keywords}
      />
      {(!isPreview || !sectionParam) && <Header />}

      {/* HERO SECTION */}
      {shouldShow('hero', content.show_hero) && (
        <section id="hero" className="relative bg-gradient-to-br from-[#1F2E4D] via-[#2D3748] to-[#1A202C] pt-20 pb-28">        
            <div className="relative z-10 container mx-auto px-6 py-6 text-center">          
            <motion.h1 initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-6xl font-bold text-white mb-6">
                {content.hero_title}
            </motion.h1>
            <motion.p initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="text-xl text-gray-300 max-w-2xl mx-auto">
                {content.hero_description}
            </motion.p>
            </div>
        </section>
      )}

      {/* CONTACT INFO CARDS */}
      {shouldShow('contact_cards', content.show_cards) && (
        <section id="contact_cards" className="py-16 bg-[#F5F6FA]">
            <div className="container mx-auto px-6">
            <div className={`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 ${shouldShow('hero', content.show_hero) ? '-mt-24' : 'mt-0'} relative z-20`}>
                {contactInfo.map((info, idx) => (
                <motion.div 
                    key={idx} 
                    whileHover={{ y: -5, scale: info.action ? 1.02 : 1 }} 
                    onClick={info.action || undefined}
                    className={`bg-white rounded-2xl p-6 shadow-xl border border-gray-100 ${info.action ? 'cursor-pointer hover:shadow-2xl transition-all duration-300' : ''}`}
                >
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
      )}

      {/* MAIN CONTENT SECTION */}
      {(shouldShow('form', content.show_form) || shouldShow('why_choose', content.show_why_choose) || shouldShow('cta', content.show_cta)) && (
        <section className="py-20 bg-white">
          <div className="container mx-auto px-6 grid lg:grid-cols-2 gap-16 max-w-7xl">
            
            {/* FORM SIDE */}
            {shouldShow('form', content.show_form) && (
              <div id="form">
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
                      <Input name="email" type="email" placeholder={content.email_placeholder} value={formData.email} onChange={handleChange} />
                  </div>
                  <div className="space-y-2">
                      <label className="text-sm font-semibold text-[#1F2E4D]">{content.company_label}</label>
                      <Input name="officeAddress" placeholder={content.company_placeholder} value={formData.officeAddress} onChange={handleChange} />
                  </div>
                  <div className="space-y-2">
                      <label className="text-sm font-semibold text-[#1F2E4D]">{content.message_label}</label>
                      <Textarea name="message" placeholder={content.message_placeholder} value={formData.message} onChange={handleChange} className="min-h-[120px] resize-none" />
                  </div>
                  <Button type="submit" className="w-full h-14 bg-[#F4B400] text-white font-bold text-lg rounded-xl shadow-lg hover:bg-[#E6A800] transition-all">
                      <Send className="w-5 h-5 mr-2" />
                      {content.form_button_text}
                  </Button>
                  </form>
              </div>
            )}

            {/* FEATURES SIDE */}
            {(shouldShow('why_choose', content.show_why_choose) || shouldShow('cta', content.show_cta)) && (
              <div className="space-y-12">
                {shouldShow('why_choose', content.show_why_choose) && (
                    <div id="why_choose">
                    <h2 className="text-4xl font-bold text-[#1F2E4D] mb-6">{content.why_title}</h2>
                    <p className="text-lg text-gray-600 leading-relaxed">{content.why_description}</p>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-8">
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
                    </div>
                )}

                {/* CTA BLOCK */}
                {shouldShow('cta', content.show_cta) && (
                    <div id="cta" className="bg-[#F4B400]/10 rounded-2xl p-8 border border-[#F4B400]/20">
                    <h3 className="text-2xl font-bold text-[#1F2E4D] mb-4">{content.cta_title}</h3>
                    <p className="text-gray-600 mb-6">{content.cta_description}</p>
                    <div className="flex flex-wrap gap-4 text-xs font-bold uppercase tracking-wider text-gray-500">
                        <span>• {content.cta_button_text1}</span>
                        <span>• {content.cta_button_text2}</span>
                        <span>• {content.cta_button_text3}</span>
                    </div>
                    </div>
                )}
              </div>
            )}
          </div>
        </section>
      )}

      {(!isPreview || !sectionParam) && <Footer />}
    </>
  );
};

export default ContactUsPage;