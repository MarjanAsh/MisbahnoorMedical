# Style sheet: Misbah Noor testimonial reel   status: provisional (waiting for your approval)

Sources: the 5 Pinterest reels you sent, saved as `reference/*.mp4` in the scratchpad. I am only learning techniques from them. I am not reusing their footage, music, logos or text.

| Ref | Pin | What it is | Length | fps |
|---|---|---|---|---|
| R1 | 2b2OwXQok | Podcast talking head, orange captions | 25.1 s | 29.97 |
| R2 | 6Dn4pwf65 | "Clean & minimal" talking head, lime captions | 16.9 s | 30 |
| R3 | 4pjdNi8E5 | Dr. Misra, doctor intro, white captions | 37.1 s | 60 |
| R4 | 5Md7IeNN8 | Doctor "no secret ingredient", white/kinetic text | 29.6 s | 30 |
| R5 | 3NVyGw5Ep | Editing-apps tutorial, yellow captions | 80.7 s | 30 |

Tags: **[measured]** = measured with ffmpeg · **[observed]** = seen in the frames · **[default]** = my choice.

## Format
- 1080×1920, 9:16, 30 fps. All refs are 9:16; 4 of the 5 are 720×1280 Pinterest copies. **[measured]**
- Target length is about 50–55 s after cutting repeats (source is 59.6 s). **[default]**

## Hook (0–3 s)
- Frame 0 is always the speaker's face, mid close-up, already talking. No logo or intro card. **[observed, all 5]**
- The first caption word appears within 0.3 s, and a **big keyword lands by about 1 s** ("BIGGEST CHALLENGE", "Prospects", "Dr. Misra", "FOUR YEARS"). **[observed]**
- R1 and R4 change the frame in the first 3 s: R4 has 3 cuts in 1.6 s (face → blurred text wall → white kinetic text), and R1 zooms out into an orbit graphic at about 2.5 s. **[measured: R4 cuts at 0.73, 1.07, 1.6 s]**
- For us: the TikTok "reply to comment" sticker is already a strong hook. Put the question **"KON SE HOSPITAL SE KARWAYA?"** big in the caption style, add a 1.0→1.12 punch-in at 0 s and a soft whoosh. **[default]**

## Pacing
- Cuts or scene changes per reel: R1 9 in 25 s (about every 2.8 s), R4 13 in 30 s (2.3 s), R5 17 in 81 s (4.7 s), R3 4 in 37 s (9 s), R2 1 in 17 s. **[measured, scene > 0.3]**
- Even with few hard cuts, the frame "changes" every **2–4 s** through punch-ins, graphics or B-roll. **[observed]**
- Our source is one take with no cuts. To get the same rhythm we use punch-ins (1.00 ↔ 1.10–1.15) at sentence breaks, plus B-roll and graphics, so something changes **every 2.5–4 s**. **[default]**

## Typography / captions (the main look)
- **Word-by-word reveal.** Small connector words appear first, then a big emphasis word pops in. There are 2–4 words on screen, often in 2 sizes, stacked on 2 lines. **[observed: R1, R2, R3, R5]**
- Font: heavy geometric sans. R1 and R5 use Black Italic in all caps, and R2 and R3 use Bold in mixed case. We will use **Inter Black / ExtraBold** (installed and licensed). **[observed → Inter is the closest]**
- Sizes on a 1080-wide frame: emphasis word about **100–120 px**, connector words about **44–56 px**. **[observed, estimated from frames]**
- Position: **chest level, about 60–68 % down the frame** (y ≈ 1150–1300 of 1920), never on the face. **[observed]**
- Highlight colour: one accent per reel. R1 uses orange #FF7A1A, R2 lime #C6FF3A with a soft glow, R5 yellow #FFD21E with a black outline, and R3 and R4 use white only. **[observed]**
  - **Our pick: warm yellow #FFD21E plus a soft glow for keywords, white for the rest.** Yellow is easy to read on the white gown and grey walls. Lime is the option if you prefer it. **[default]**
- Treatment: no box. A soft drop shadow (0 4 px 18 px, 60 % black) and a 3 px dark stroke on yellow. **[observed R5/R2]**
- Animation: the active word pops 0.6 → 1.08 → 1.0 in about 0.18 s (power3.out). The previous words stay and the group clears on a phrase break. **[estimated from consecutive frames]**
- Brand spelling: **"Dogar Sajji"** everywhere. Also "Misbah Noor", "Dr. Hina Ahmed", "Ali Town", "Thokar Niaz Baig".

## Palette (measured mean luma / saturation, 0–255)
- R1 99/14, R3 99/13, R5 91/12, R2 55/7 (dark, moody), R4 169/6 (bright white). Most refs sit at **mid exposure with low to moderate saturation**, so they look rich but not loud. **[measured]**
- Warm skin, neutral to warm whites, gently lifted blacks (no pure black in R1, R3 or R5). **[observed]**

## Framing / B-roll / zooms
- Mid close-up of a single speaker, eyes on the upper third. **[observed]**
- B-roll and inserts: R4 uses full-screen kinetic text cards and a PiP card with rounded corners and a drop shadow. R5 uses a ring timer ("59s"). R2 uses a REC viewfinder frame and UI chips. R1 uses an orbit graphic with avatar chips. **[observed]**
- For us: 3 full-screen B-roll inserts of **2–2.5 s** each (Muse), with captions continuing over them. There are also 4 graphic moments: a location pin chip, a Dr. name lower-third, a "24 GHANTE" ring and a "100% RECOMMENDED" badge. **[default]**
- Zooms: punch-ins of **1.10–1.15×**, either hard cuts or a 0.25 s ease. Faces stay centred. **[observed/estimated]**

## Motion
- Pops at 0.15–0.25 s with power3.out, chips slide up 40 px and fade in over 0.3 s, and the B-roll transition is a 6-frame zoom-blur or a straight cut. **[estimated]**
- R2 uses a "glitch / stripe" transition once. It is too techy for a medical testimonial, so **we skip it**. **[default]**

## Colour (our grade)
- A Sony FX3 / A7S III style: even exposure, a soft S-curve with lifted blacks (out-black ≈ 16–20), highlight roll-off, skin pushed slightly warm, cyan/green walls desaturated slightly, overall saturation +5–8 % (not more), light grain, **no sharpening**. **[default, from your brief]**
- Limitation: the source is a **576×1024 phone recording**, so 1080×1920 export is an upscale (lanczos plus light denoise). It will look clean, but it cannot have true camera-level detail.

## Audio
- Integrated loudness: R1 −14.2, R4 −14.4, R2 −14.9, R3 −17.8, R5 −20.9 LUFS. **[measured]**
- **Target −14 LUFS**, true peak ≤ −1 dBTP. **[default, social]**
- Music: a soft warm ambient bed, **−18 to −20 dB under the voice** and ducked while she talks. I generate it myself, so there are no licensing issues. SFX: a soft whoosh on B-roll entries and a light pop/ding on the badge, at least 12 dB under the voice. **[default]**

## Do / Don't
- Do keep her voice clear and first. Captions must be exact, and the brand names must be spelled right.
- Don't make AI B-roll that looks like the real Misbah Noor building, a real doctor's face, or the actual patient. The B-roll is generic (hands, corridor, newborn), so it does not mislead viewers about the hospital.
- Don't use glitch effects, over-saturation, crushed blacks or sharpening.

## Open questions
1. Accent colour: **yellow** (my pick) or **lime green**?
2. Do you want the hospital phone number or WhatsApp number on the end card?
