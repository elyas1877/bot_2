export PATH=${PATH}:${PWD}/../boost
export BOOST_ROOT=${PWD}/../boost
export BOOST_BUILD_PATH=${PWD}/../boost/tools/build
# when building b2, we don't want sanitizers enabled
ASAN_OPTIONS=detect_leaks=0
(cd ${PWD}/../boost && ./bootstrap.sh && ./b2 headers)

echo "CXX=$CXX"
echo "CXXFLAGS=$CXXFLAGS"

echo "using clang : ossfuzz : $CXX : <compileflags>\"$CXXFLAGS\" <linkflags>\"$CXXFLAGS\" <linkflags>\"${LIB_FUZZING_ENGINE}\" ;" >project-config.jam
cat project-config.jam
cd fuzzers
# we don't want sanitizers enabled on b2 itself
ASAN_OPTIONS=detect_leaks=0 b2 clang-ossfuzz -j$(nproc) crypto=openssl fuzz=external sanitize=off stage-large logging=off
cp fuzzers/* $OUT

wget --no-verbose https://github.com/arvidn/libtorrent/releases/download/2.0/corpus.zip
unzip -q corpus.zip
cd corpus
for f in *; do
zip -q -r ${OUT}/fuzzer_${f}_seed_corpus.zip ${f}
done