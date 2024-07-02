git clone https://github.com/levihsu/OOTDiffusion.git
cd OOTDiffusion
rm -rf .git*
# touch ttt.txt
conda create -n ootd python==3.10
conda activate ootd
pip3 install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2
pip3 install -r requirements.txt
git lfs install
cd checkpoints
git clone https://huggingface.co/levihsu/OOTDiffusion
mv ./OOTDiffusion/checkpoints/* ./
rm -rf ./OOTDiffusion
git clone https://huggingface.co/openai/clip-vit-large-patch14
cd clip-vit-large-patch14
rm -rf .git*

