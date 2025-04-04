#include <string>
#include <boost/filesystem/path.hpp>

namespace vega_config {
    struct Config {
        explicit Config(const std::string& json_text);

        void load_config(const std::string& json_text);
        void load_config(const boost::filesystem::path& config_file_path);

// JsonStruct
    };

    extern std::shared_ptr<Config> config;
}
