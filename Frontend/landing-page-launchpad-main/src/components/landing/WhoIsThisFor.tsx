import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Store, ShoppingBag, Pill, Wrench, TrendingUp } from "lucide-react";
import { fetchStoreTypes } from "@/services/api";
import { fetchLandingPageContent, LandingPageContent } from "@/services/api";

const iconMap: any = {
  store: Store,
  shopping: ShoppingBag,
  medical: Pill,
  hardware: Wrench,
  growth: TrendingUp,
};

const WhoIsThisFor = () => {
  const [content, setContent] = useState<LandingPageContent | null>(null);
  const [livePreview, setLivePreview] = useState<any>(null);
  const [types, setTypes] = useState<any[]>([]);

  // Load section headings from LandingPageContent
  useEffect(() => {
    const loadContent = async () => {
      const data = await fetchLandingPageContent();
      if (data) setContent(data);
    };
    loadContent();
  }, []);

  // Fetch store types from API
  useEffect(() => {
    const loadStoreTypes = async () => {

      try {

        const res = await fetch("/api/store-types/");
        const data = await res.json();

        setTypes(data);

      } catch (err) {

        console.error("Error loading store types", err);

      }

    };
    loadStoreTypes();
  }, []);

  // Live preview listener
  useEffect(() => {
    const previewChannel = new BroadcastChannel('aisetu_preview');

    const handler = (event: any) => {
      if (event.data && typeof event.data === 'object' && event.data.source === 'django-admin') {
        const payload = event.data.payload;
        
        if (event.data.model === 'LandingPageContent' || event.data.model === 'WhoIsThisForContent') {
          setContent((prev: any) => ({ ...prev, ...payload }));
        } else if (event.data.model === 'StoreType') {
          const pk = event.data.pk;
          setTypes(prev => prev.map(t => (t.id === parseInt(pk) || t.id === pk) ? { ...t, ...payload } : t));
        }

        // Broadcast to other tabs
        previewChannel.postMessage({
          type: 'LIVE_PREVIEW_UPDATE',
          model: event.data.model,
          pk: event.data.pk,
          content: payload
        });
      }
    };

    const channelHandler = (event: MessageEvent) => {
      if (event.data?.type === 'LIVE_PREVIEW_UPDATE') {
        const { model, content: payload, pk } = event.data;
        if (model === 'LandingPageContent' || model === 'WhoIsThisForContent') {
          setContent((prev: any) => ({ ...prev, ...payload }));
        } else if (model === 'StoreType') {
          setTypes(prev => prev.map(t => (t.id === parseInt(pk) || t.id === pk) ? { ...t, ...payload } : t));
        }
      }
    };

    window.addEventListener("message", handler);
    previewChannel.addEventListener("message", channelHandler);

    return () => {
      window.removeEventListener("message", handler);
      previewChannel.removeEventListener("message", channelHandler);
      previewChannel.close();
    };
  }, []);

  return (
    <section className="py-16 lg:py-24 bg-secondary">
      <div className="container">
        {/* Section Header */}
        <div className="text-center mb-12">
          <span className="text-accent font-semibold text-sm uppercase tracking-wider">
            {content?.who_main_title || "Perfect For"}
          </span>

          <h2 className="text-3xl lg:text-4xl font-bold mt-2 text-foreground">
            {content?.who_title || "Who Is This For?"}
          </h2>
        </div>

        {/* Store Type Cards */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
          {(content?.store_types || types).map((t, i) => {
            const Icon = iconMap[t.icon];
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.08 }}
                className="bg-card rounded-xl p-6 text-center shadow-card border border-border hover:shadow-card-hover transition-shadow"
              >
                <div className="w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center mx-auto mb-3 overflow-hidden">
                  {t.image ? (
                    <img src={t.image} alt={t.title} className="w-full h-full object-cover" />
                  ) : (
                    Icon && <Icon className="h-7 w-7 text-primary" />
                  )}
                </div>

                <h3 className="font-heading font-semibold text-sm text-foreground">
                  {t.title}
                </h3>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default WhoIsThisFor;