# 🌐 ZION Domain Configuration

**Primary Domain:** www.zionterranova.com  
**Updated:** 29. října 2025

---

## 🏠 Main Domains

### Production
- **Main Website:** https://www.zionterranova.com
- **Pool:** https://pool.zionterranova.com
- **Explorer:** https://explorer.zionterranova.com
- **API:** https://api.zionterranova.com
- **Documentation:** https://docs.zionterranova.com

### Testnet
- **Testnet Website:** https://testnet.zionterranova.com
- **Testnet Faucet:** https://testnet-faucet.zionterranova.com
- **Testnet Pool:** https://testnet-pool.zionterranova.com
- **Testnet Explorer:** https://testnet-explorer.zionterranova.com

---

## 📧 Email Configuration

### Official Emails
- **General:** info@zionterranova.com
- **Support:** support@zionterranova.com
- **Security:** security@zionterranova.com
- **Development:** dev@zionterranova.com
- **Press:** press@zionterranova.com
- **Partnerships:** partnerships@zionterranova.com

---

## 🔗 Social Media

### Official Channels
- **Twitter/X:** https://twitter.com/zionterranova
- **Telegram:** https://t.me/zionblockchain
- **Discord:** https://discord.gg/zion
- **GitHub:** https://github.com/estrelaisabellazion3/Zion-2.8
- **Medium:** https://medium.com/@zionterranova
- **YouTube:** https://youtube.com/@zionterranova

---

## 🌍 DNS Configuration (For DevOps)

### A Records
```
www.zionterranova.com      → 91.98.122.165
pool.zionterranova.com     → 91.98.122.165
api.zionterranova.com      → 91.98.122.165
testnet.zionterranova.com  → 91.98.122.165
```

### CNAME Records
```
explorer.zionterranova.com → www.zionterranova.com
docs.zionterranova.com     → www.zionterranova.com
```

### MX Records (Email)
```
zionterranova.com  MX 10 mail.zionterranova.com
```

---

## 🔒 SSL/TLS Certificates

### Certificate Authority
- **Provider:** Let's Encrypt / Cloudflare
- **Auto-renewal:** Enabled
- **Wildcard:** *.zionterranova.com

### HTTPS Enforcement
- All HTTP traffic redirects to HTTPS
- HSTS enabled (max-age: 31536000)
- TLS 1.2+ required

---

## 📝 Migration Notes

### Old Domain References (To Update)
- ~~zion-blockchain.org~~ → **www.zionterranova.com**
- ~~pool.zion-blockchain.org~~ → **pool.zionterranova.com**
- ~~api.zion-blockchain.org~~ → **api.zionterranova.com**

### Files Updated (29.10.2025)
- ✅ `Readme.md` - Main website links
- ✅ `docs/TESTNET_RELEASE_PLAN_v2.8.3.md` - All domain references
- ✅ `website/index.html` - Social links
- ✅ `docs/DOMAIN_CONFIG.md` - This file (created)

### Pending Updates
- [ ] `docs/COMMUNITY_LAUNCH_MATERIALS.md` - Pool URLs
- [ ] `docs/MULTI_ALGORITHM_MINING_GUIDE.md` - Pool endpoints
- [ ] `docs/BRAND_GUIDELINES.md` - Official domains
- [ ] `.env.production` - Domain environment variables
- [ ] Marketing materials
- [ ] Social media profiles

---

## 🚀 Domain Launch Checklist

### Pre-Launch
- [ ] Domain registered and verified
- [ ] DNS records configured
- [ ] SSL certificates installed
- [ ] Email accounts created
- [ ] Cloudflare configured (if using)

### Post-Launch
- [ ] Update all documentation
- [ ] Update social media links
- [ ] Announce new domain on Discord/Telegram
- [ ] Update GitHub repo description
- [ ] Update CoinMarketCap/CoinGecko listings
- [ ] Set up redirects from old domains (if any)

---

## 📊 Analytics & Monitoring

### Tools
- **Google Analytics:** GA4 property for www.zionterranova.com
- **Cloudflare Analytics:** Traffic and security monitoring
- **Uptime Monitoring:** UptimeRobot / Pingdom
- **SSL Monitoring:** SSL Labs / Qualys

### Key Metrics
- Page load time: < 2s
- SSL rating: A+
- Uptime: 99.9%
- Security headers: All A grades

---

## 🛡️ Security

### DNSSEC
- Enabled on all domains
- Key rotation: Annual

### SPF Record
```
v=spf1 include:_spf.zionterranova.com ~all
```

### DKIM Record
```
default._domainkey.zionterranova.com TXT "v=DKIM1; k=rsa; p=..."
```

### DMARC Record
```
_dmarc.zionterranova.com TXT "v=DMARC1; p=quarantine; rua=mailto:security@zionterranova.com"
```

---

## 📞 Support

For domain-related issues:
- **Technical:** dev@zionterranova.com
- **Security:** security@zionterranova.com
- **General:** info@zionterranova.com

---

**Last Updated:** 29. října 2025  
**Next Review:** 29. listopadu 2025
