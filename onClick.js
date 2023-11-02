import { ethers } from 'ethers';

// Assume you have the contract ABI and address
const contractABI = [...]  // Your contract ABI here
const contractAddress = "0x...";  // Your contract address here


async function onClick(candidateId) {

    let provider;
    let signer;
    let contract;

    if (typeof window.ethereum !== 'undefined') {
        provider = new ethers.providers.Web3Provider(window.ethereum);
        signer = provider.getSigner();
        contract = new ethers.Contract(contractAddress, contractABI, signer);
    } else {
        console.error("Please install MetaMask!");
    }

    try {
        const txResponse = await contract.vote(candidateId);
        console.log("Transaction sent:", txResponse);
        
        // Wait for the transaction to be mined
        const receipt = await txResponse.wait();
        console.log("Transaction confirmed:", receipt);
        
        // Optionally, retrieve and log the updated vote count
        const updatedVoteCount = await contract.candidates(candidateId);
        console.log("Updated vote count:", updatedVoteCount.voteCount.toString());
    } catch (error) {
        console.error("Error:", error);
    }
}



// Create a signer
const privateKey = process.env.PRIVATE_KEY;
const signer = new ethers.Wallet(privateKey, provider);

// Get contract ABI and address
const abi = contract.abi;
const contractAddress2 = '0xA4766Ceb9E84a71D282A4CED9fB8Fe93C49b2Ff7';

// Create a contract instance
const myNftContract = new ethers.Contract(contractAddress2, abi, signer);

// Get the NFT Metadata IPFS URL
const tokenUri = "https://gateway.pinata.cloud/ipfs/QmYueiuRNmL4MiA2GwtVMm6ZagknXnSpQnB3z2gWbz36hP";

// Call mintNFT function
const mintNFT = async () => {
    let nftTxn = await myNftContract.mintNFT(signer.address, tokenUri);
    await nftTxn.wait();
    console.log(`NFT Minted!👍`);
};

mintNFT()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
