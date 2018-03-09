. /volume1/moindev/.env/ridibooks_hls/bin/activate
export PYTHONPATH=/volume1/moindev/lib:$PYTHONPATH
python /volume1/moindev/lib/moin/bin/ridi.py delta $1 --dayone --color yellow
