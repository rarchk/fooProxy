echo "#INSTALLING DEPENDENCIES"
echo "========================"
cat requirements.txt 
pip install -r requirements.txt > /dev/null
echo "#Starting foo Proxy"
echo "======================="
python foo.py
 
