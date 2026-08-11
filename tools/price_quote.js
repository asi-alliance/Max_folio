const { ethers } = require('/home/nartech/Iter/node_modules/ethers');
const { getOracleDeployment } = require('/home/nartech/Iter/node_modules/sfi-oracle-sdk/dist/cjs');
const abis = require('/home/nartech/Iter/node_modules/sfi-oracle-sdk/dist/cjs/generated/abis.js');
const chainId = 8453;
const d = getOracleDeployment(chainId);
const rpc = 'https://mainnet.base.org';
const p = new ethers.JsonRpcProvider(rpc, chainId);
const ro = new ethers.Contract(d.referenceAssetOracle, abis.referenceAssetOracleAbi, p);
const cl = new ethers.Contract(d.chainlinkOracle, abis.chainlinkOracleAbi, p);
const rg = new ethers.Contract(d.oracleRegistry, abis.oracleRegistryAbi, p);

async function main() {
  const token = process.argv[2] || 'BTC';
  const USDC = await cl.USDC();
  const REF_PREC = await cl.REFERENCE_PRECISION();
  let addr;
  if (token.startsWith('0x')) {
    addr = token;
  } else if (token === 'BTC') addr = await cl.BTC();
  else if (token === 'ETH') addr = await cl.ETH();
  else if (token === 'WBTC') addr = await cl.WBTC();
  else if (token === 'WETH') addr = await cl.WETH();
  else { console.error('Unknown token:', token, 'Supported: BTC, ETH, WBTC, WETH, or 0xADDRESS'); process.exit(1); }
  const hasOracle = await rg.hasOracle(addr);
  const [price, oldest] = await ro.getPrice.staticCall(addr, USDC);
  const usdPrice = Number(price) / Number(REF_PREC);
  console.log(JSON.stringify({ token, address: addr, usd_price: usdPrice, raw_price: price.toString(), oldest_timestamp: oldest.toString(), chain: 'base', registered_oracle: hasOracle }));
}
main().then(() => process.exit(0)).catch(e => { console.error('FATAL:', e.message.substring(0,400)); process.exit(1); });
