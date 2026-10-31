import sharp from 'sharp';
import fs from 'fs';
import path from 'path';

const userLogoPath = '/Users/zaheerabbas/.gemini/antigravity/brain/1a8a20f9-60ed-45dc-8c06-7e0a1c39dc90/.user_uploaded/media_1793456183301_b30ada05.png';
const imagesDir = path.resolve('public/assets/images');
const publicDir = path.resolve('public');

async function processLogos() {
  console.log('Processing logos from:', userLogoPath);

  // 1. Copy pristine original logo to public/assets/images/prana-solutions-logo.png
  const originalBuffer = fs.readFileSync(userLogoPath);
  fs.writeFileSync(path.join(imagesDir, 'prana-solutions-logo.png'), originalBuffer);
  console.log('Saved prana-solutions-logo.png');

  // Overwrite legacy filenames for backwards-compatibility
  fs.writeFileSync(path.join(imagesDir, 'Prana-Logo-.png'), originalBuffer);
  fs.writeFileSync(path.join(imagesDir, 'prana-Logo.png'), originalBuffer);
  fs.writeFileSync(path.join(imagesDir, 'prana-Logo-300x50.png'), originalBuffer);
  fs.writeFileSync(path.join(imagesDir, 'cropped-PST_LOGORemovebg.png'), originalBuffer);
  fs.writeFileSync(path.join(imagesDir, 'PST_LOGORemovebg.png'), originalBuffer);
  console.log('Updated legacy logo files with the official logo');

  // 2. Generate dark-background / footer variant (white text for 'PRANA SOLUTIONS TECH', vibrant motif intact)
  const { data, info } = await sharp(userLogoPath).raw().toBuffer({ resolveWithObject: true });
  const darkBgBuffer = Buffer.from(data);

  for (let y = 0; y < info.height; y++) {
    for (let x = 0; x < info.width; x++) {
      const idx = (y * info.width + x) * info.channels;
      const alpha = darkBgBuffer[idx + 3];
      // Text starts around x >= 83
      if (alpha > 10 && x >= 83) {
        darkBgBuffer[idx] = 255;     // R
        darkBgBuffer[idx + 1] = 255; // G
        darkBgBuffer[idx + 2] = 255; // B
      }
    }
  }

  await sharp(darkBgBuffer, { raw: { width: info.width, height: info.height, channels: info.channels } })
    .png()
    .toFile(path.join(imagesDir, 'prana-solutions-logo-white.png'));
  console.log('Saved prana-solutions-logo-white.png');

  // 3. Extract the emblem / icon mark (flame/leaf motif) for favicon & square icons
  // Bounds measured: x: [23, 82], y: [14, 109], w: 60, h: 96
  const emblemWidth = 83 - 23;
  const emblemHeight = 110 - 14;

  const croppedEmblem = await sharp(userLogoPath)
    .extract({ left: 23, top: 14, width: emblemWidth, height: emblemHeight })
    .toBuffer();

  // Create square icon with balanced padding on transparent background
  const iconSize = 512;
  const targetHeight = Math.round(iconSize * 0.85); // 85% height
  const targetWidth = Math.round((targetHeight / emblemHeight) * emblemWidth);

  const resizedEmblem = await sharp(croppedEmblem)
    .resize(targetWidth, targetHeight, { fit: 'contain' })
    .toBuffer();

  const squareIconBuffer = await sharp({
    create: {
      width: iconSize,
      height: iconSize,
      channels: 4,
      background: { r: 0, g: 0, b: 0, alpha: 0 }
    }
  })
  .composite([{ input: resizedEmblem, gravity: 'center' }])
  .png()
  .toBuffer();

  // Save app icons
  fs.writeFileSync(path.join(publicDir, 'favicon.png'), await sharp(squareIconBuffer).resize(32, 32).png().toBuffer());
  fs.writeFileSync(path.join(publicDir, 'apple-touch-icon.png'), await sharp(squareIconBuffer).resize(180, 180).png().toBuffer());
  fs.writeFileSync(path.join(imagesDir, 'prana-icon.png'), squareIconBuffer);

  // Create SVG favicon wrapping the high-res emblem mark
  const emblemBase64 = squareIconBuffer.toString('base64');
  const svgFavicon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <image href="data:image/png;base64,${emblemBase64}" width="512" height="512"/>
</svg>
`;
  fs.writeFileSync(path.join(publicDir, 'favicon.svg'), svgFavicon);
  console.log('Saved favicon.svg, favicon.png, apple-touch-icon.png, and prana-icon.png');
}

processLogos().catch((err) => {
  console.error('Error processing logos:', err);
  process.exit(1);
});

